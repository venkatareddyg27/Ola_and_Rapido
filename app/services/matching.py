# matching.py

import math
import asyncio

from uuid import UUID
from typing import List, Dict, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_models import DriverProfile, User,DriverLocation
from app.models.vehicles import Vehicle
from app.models.trips import Trip
from app.core.enums import DriverStatus, DriverOnTripStatus, TripStatus


# =========================================================
# CONFIG
# =========================================================

DEFAULT_RADIUS_KM = 5
MAX_DRIVER_REQUESTS = 3
REQUEST_TIMEOUT = 30

# Radius expansion steps when no drivers are found (km)
RADIUS_EXPANSION_STEPS = [5, 10, 15]

# Weight applied to rating in driver scoring (0-1)
RATING_WEIGHT = 0.3


# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    """
    Haversine formula — returns distance in km.
    """
    radius = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius * c


def bounding_box(lat: float, lng: float, radius_km: float):
    """
    Returns (min_lat, max_lat, min_lng, max_lng) for a rough
    bounding box around (lat, lng) with the given radius.
    Used as a cheap SQL pre-filter before the exact Haversine check.
    """
    lat_delta = radius_km / 111.0
    lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
    return (
        lat - lat_delta,
        lat + lat_delta,
        lng - lng_delta,
        lng + lng_delta,
    )


def driver_score(distance: float, rating: float, radius_km: float) -> float:
    """
    Lower score = better match.
    Blends normalised distance and inverse rating so both contribute.
    """
    normalised_distance = distance / radius_km          # 0..1
    normalised_rating   = 1.0 - (rating / 5.0)         # 0..1, lower = better
    return (1 - RATING_WEIGHT) * normalised_distance + RATING_WEIGHT * normalised_rating


# =========================================================
# MATCHING SERVICE
# =========================================================

class DriverMatchingService:

    def __init__(
        self,
        db: AsyncSession,
        redis_client=None,
        websocket_manager=None,
    ):
        self.db = db
        self.redis = redis_client
        self.websocket_manager = websocket_manager

    # =====================================================
    # FIND NEARBY DRIVERS
    # =====================================================

    async def find_nearby_drivers(
        self,
        pickup_lat: float,
        pickup_lng: float,
        vehicle_category: str,
        radius_km: int = DEFAULT_RADIUS_KM,
    ) -> List[Dict]:

        matched_drivers = []

        min_lat, max_lat, min_lng, max_lng = bounding_box(
            pickup_lat, pickup_lng, radius_km
        )

        # --------------------------------------------------
        # Single query: drivers + vehicle + latest location
        # --------------------------------------------------
        # Subquery: most-recent location id per driver
        latest_loc_subq = (
            select(DriverLocation.id)
            .where(DriverLocation.driver_id == DriverProfile.id)
            .order_by(DriverLocation.updated_at.desc())
            .limit(1)
            .correlate(DriverProfile)
            .scalar_subquery()
        )

        result = await self.db.execute(
            select(DriverProfile, User, Vehicle, DriverLocation)
            .join(User,     DriverProfile.user_id   == User.id)
            .join(Vehicle,  DriverProfile.vehicle_id == Vehicle.id)
            .join(
                DriverLocation,
                DriverLocation.id == latest_loc_subq,
            )
            .where(
                DriverProfile.status == DriverStatus.ONLINE,
                Vehicle.category     == vehicle_category,
                DriverLocation.latitude.between(min_lat, max_lat),
                DriverLocation.longitude.between(min_lng, max_lng),
            )
        )

        rows = result.all()

        # --------------------------------------------------
        # Exact Haversine filter + scoring
        # --------------------------------------------------
        for driver, user, vehicle, location in rows:

            distance = calculate_distance(
                pickup_lat,
                pickup_lng,
                float(location.latitude),
                float(location.longitude),
            )

            if distance > radius_km:
                continue

            rating = float(driver.rating or 5)

            matched_drivers.append({
                "driver_id":  str(driver.id),
                "user_id":    str(user.id),
                "vehicle_id": str(vehicle.id),
                "distance":   round(distance, 2),
                "rating":     rating,
                "total_trips": driver.total_trips,
                "latitude":   float(location.latitude),
                "longitude":  float(location.longitude),
                "score":      driver_score(distance, rating, radius_km),
            })

        # Lower score = better
        matched_drivers.sort(key=lambda x: x["score"])

        return matched_drivers

    # =====================================================
    # SEND RIDE REQUESTS
    # =====================================================

    async def send_ride_requests(
        self,
        trip_id: UUID,
        drivers: List[Dict],
    ) -> Optional[str]:

        if not drivers:
            return None

        selected_drivers = drivers[:MAX_DRIVER_REQUESTS]
        notified_user_ids = [d["user_id"] for d in selected_drivers]

        # --------------------------------------------------
        # Save matching state
        # --------------------------------------------------
        if self.redis:
            await self.redis.set(
                f"trip_matching:{trip_id}",
                "SEARCHING",
                ex=60,
            )

        # --------------------------------------------------
        # Send requests
        # --------------------------------------------------
        for driver in selected_drivers:
            payload = {
                "event":    "NEW_RIDE_REQUEST",
                "trip_id":  str(trip_id),
                "distance": driver["distance"],
            }

            if self.websocket_manager:
                await self.websocket_manager.send_to_user(
                    user_id=driver["user_id"],
                    message=payload,
                )

        # --------------------------------------------------
        # Wait for acceptance
        # --------------------------------------------------
        accepted_driver = await self.wait_for_acceptance(trip_id=trip_id)

        # --------------------------------------------------
        # Cancel only the drivers who were actually notified
        # --------------------------------------------------
        if accepted_driver:
            await self.cancel_other_requests(
                trip_id=trip_id,
                accepted_driver_id=accepted_driver,
                notified_user_ids=notified_user_ids,
            )

        return accepted_driver

    # =====================================================
    # WAIT FOR DRIVER ACCEPTANCE
    # =====================================================

    async def wait_for_acceptance(
        self,
        trip_id: UUID,
    ) -> Optional[str]:

        channel = f"trip_accept_ch:{trip_id}"

        if self.redis:
            # BLPOP blocks up to REQUEST_TIMEOUT seconds; returns
            # (key, value) or None on timeout.
            result = await self.redis.blpop(channel, timeout=REQUEST_TIMEOUT)
            if result:
                _, value = result
                return value.decode() if isinstance(value, bytes) else value
            return None

        # Fallback: simple polling (no Redis)
        for _ in range(REQUEST_TIMEOUT):
            await asyncio.sleep(1)
        return None

    # =====================================================
    # ACCEPT RIDE
    # =====================================================

    async def accept_ride(
        self,
        trip_id: UUID,
        driver_id: UUID,
    ) -> bool:

        if not self.redis:
            raise RuntimeError("Redis is required for accept_ride")

        redis_key     = f"trip_accepted:{trip_id}"
        accept_channel = f"trip_accept_ch:{trip_id}"

        # Atomic: only succeeds if the key does not yet exist
        claimed = await self.redis.set(
            redis_key,
            str(driver_id),
            ex=300,
            nx=True,  # NX = set only if Not eXists
        )

        if not claimed:
            # Another driver already accepted
            return False

        # --------------------------------------------------
        # Update trip in DB
        # --------------------------------------------------
        result = await self.db.execute(
            select(Trip).where(Trip.id == trip_id)
        )
        trip = result.scalars().first()

        if not trip:
            # Stale trip — roll back the Redis claim
            await self.redis.delete(redis_key)
            return False

        trip.driver_id = driver_id
        trip.status    = TripStatus.DRIVER_ASSIGNED

        # --------------------------------------------------
        # Update driver status so they stop appearing in searches
        # --------------------------------------------------
        driver_result = await self.db.execute(
            select(DriverProfile).where(DriverProfile.id == driver_id)
        )
        driver_profile = driver_result.scalars().first()

        if driver_profile:
            driver_profile.status = DriverStatus.ON_TRIP

        await self.db.commit()

        # --------------------------------------------------
        # Notify wait_for_acceptance via pub/sub channel
        # --------------------------------------------------
        await self.redis.lpush(accept_channel, str(driver_id))
        await self.redis.expire(accept_channel, 60)

        return True

    # =====================================================
    # REJECT RIDE
    # =====================================================

    async def reject_ride(
        self,
        trip_id: UUID,
        driver_id: UUID,
    ):
        if self.redis:
            await self.redis.set(
                f"trip_rejected:{trip_id}:{driver_id}",
                "REJECTED",
                ex=300,
            )

    # =====================================================
    # CANCEL OTHER REQUESTS
    # =====================================================

    async def cancel_other_requests(
        self,
        trip_id: UUID,
        accepted_driver_id: str,
        notified_user_ids: List[str],
    ):

        payload = {
            "event":   "RIDE_REQUEST_CANCELLED",
            "trip_id": str(trip_id),
        }

        if not self.websocket_manager:
            return

        for user_id in notified_user_ids:
            if user_id == accepted_driver_id:
                continue
            await self.websocket_manager.send_to_user(
                user_id=user_id,
                message=payload,
            )

    # =====================================================
    # MAIN MATCHING FLOW
    # =====================================================

    async def match_driver(
        self,
        trip_id: UUID,
        pickup_lat: float,
        pickup_lng: float,
        vehicle_category: str,
    ) -> Optional[str]:
        for radius_km in RADIUS_EXPANSION_STEPS:

            nearby_drivers = await self.find_nearby_drivers(
                pickup_lat=pickup_lat,
                pickup_lng=pickup_lng,
                vehicle_category=vehicle_category,
                radius_km=radius_km,
            )

            if not nearby_drivers:
                # No drivers in this radius — try a wider radius
                continue

            accepted_driver = await self.send_ride_requests(
                trip_id=trip_id,
                drivers=nearby_drivers,
            )

            if accepted_driver:
                return accepted_driver

            # No one accepted — try wider radius with fresh drivers

        return None