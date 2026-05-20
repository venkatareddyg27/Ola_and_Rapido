# matching.py

import math
import asyncio

from uuid import UUID
from typing import List, Dict, Optional

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.users import (
    DriverProfile,
    User
)

from app.models.vehicles import (
    Vehicle
)

from app.models.trips import (
    Trip
)

from app.models.users import (
    DriverLocation
)

from app.core.enums import (
    DriverStatus,
    TripStatus
)

# =========================================================
# CONFIG
# =========================================================

DEFAULT_RADIUS_KM = 5

MAX_DRIVER_REQUESTS = 3

REQUEST_TIMEOUT = 30


# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Haversine formula
    """

    radius = 6371

    dlat = math.radians(
        lat2 - lat1
    )

    dlon = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(math.radians(lat1))
        *
        math.cos(math.radians(lat2))
        *
        math.sin(dlon / 2) ** 2
    )

    c = (
        2 *
        math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )
    )

    return radius * c


# =========================================================
# MATCHING SERVICE
# =========================================================

class DriverMatchingService:

    def __init__(
        self,
        db: AsyncSession,
        redis_client=None,
        websocket_manager=None
    ):

        self.db = db

        self.redis = redis_client

        self.websocket_manager = (
            websocket_manager
        )

    # =====================================================
    # FIND NEARBY DRIVERS
    # =====================================================

    async def find_nearby_drivers(
        self,
        pickup_lat: float,
        pickup_lng: float,
        vehicle_category: str,
        radius_km: int = (
            DEFAULT_RADIUS_KM
        )
    ) -> List[Dict]:

        matched_drivers = []

        # =================================================
        # GET ONLINE DRIVERS
        # =================================================

        result = await self.db.execute(

            select(
                DriverProfile,
                User,
                Vehicle
            )
            .join(
                User,
                DriverProfile.user_id ==
                User.id
            )
            .join(
                Vehicle,
                DriverProfile.vehicle_id ==
                Vehicle.id
            )
            .where(
                DriverProfile.status ==
                DriverStatus.ONLINE,

                Vehicle.category ==
                vehicle_category
            )
        )

        drivers = result.all()

        # =================================================
        # FILTER BY DISTANCE
        # =================================================

        for (
            driver,
            user,
            vehicle
        ) in drivers:

            location_result = (
                await self.db.execute(
                    select(
                        DriverLocation
                    )
                    .where(
                        DriverLocation.driver_id ==
                        driver.id
                    )
                    .order_by(
                        DriverLocation.updated_at.desc()
                    )
                )
            )

            location = (
                location_result
                .scalars()
                .first()
            )

            if not location:
                continue

            distance = (
                calculate_distance(
                    pickup_lat,
                    pickup_lng,

                    float(location.latitude),
                    float(location.longitude)
                )
            )

            if distance > radius_km:
                continue

            matched_drivers.append({

                "driver_id": str(
                    driver.id
                ),

                "user_id": str(
                    user.id
                ),

                "vehicle_id": str(
                    vehicle.id
                ),

                "distance": round(
                    distance,
                    2
                ),

                "rating": float(
                    driver.rating or 5
                ),

                "total_trips": (
                    driver.total_trips
                ),

                "latitude": float(
                    location.latitude
                ),

                "longitude": float(
                    location.longitude
                )
            })

        # =================================================
        # SORT BY DISTANCE + RATING
        # =================================================

        matched_drivers.sort(
            key=lambda x: (
                x["distance"],
                -x["rating"]
            )
        )

        return matched_drivers

    # =====================================================
    # SEND RIDE REQUESTS
    # =====================================================

    async def send_ride_requests(
        self,
        trip_id: UUID,
        drivers: List[Dict]
    ) -> Optional[str]:

        if not drivers:
            return None

        selected_drivers = (
            drivers[:MAX_DRIVER_REQUESTS]
        )

        # =================================================
        # SAVE MATCHING STATE
        # =================================================

        if self.redis:

            await self.redis.set(
                f"trip_matching:{trip_id}",
                "SEARCHING",
                ex=60
            )

        # =================================================
        # SEND REQUESTS
        # =================================================

        for driver in selected_drivers:

            payload = {

                "event":
                "NEW_RIDE_REQUEST",

                "trip_id":
                str(trip_id),

                "distance":
                driver["distance"]
            }

            if self.websocket_manager:

                await (
                    self.websocket_manager
                    .send_to_user(
                        user_id=(
                            driver["user_id"]
                        ),
                        message=payload
                    )
                )

        # =================================================
        # WAIT FOR ACCEPTANCE
        # =================================================

        accepted_driver = (
            await self.wait_for_acceptance(
                trip_id=trip_id
            )
        )

        # =================================================
        # CANCEL OTHER REQUESTS
        # =================================================

        if accepted_driver:

            await (
                self.cancel_other_requests(
                    trip_id=trip_id,
                    accepted_driver_id=(
                        accepted_driver
                    )
                )
            )

        return accepted_driver

    # =====================================================
    # WAIT FOR DRIVER ACCEPTANCE
    # =====================================================

    async def wait_for_acceptance(
        self,
        trip_id: UUID
    ) -> Optional[str]:

        for _ in range(
            REQUEST_TIMEOUT
        ):

            if self.redis:

                accepted_driver = (
                    await self.redis.get(
                        f"trip_accepted:{trip_id}"
                    )
                )

                if accepted_driver:

                    if isinstance(
                        accepted_driver,
                        bytes
                    ):
                        return (
                            accepted_driver
                            .decode()
                        )

                    return accepted_driver

            await asyncio.sleep(1)

        return None

    # =====================================================
    # ACCEPT RIDE
    # =====================================================

    async def accept_ride(
        self,
        trip_id: UUID,
        driver_id: UUID
    ) -> bool:

        redis_key = (
            f"trip_accepted:{trip_id}"
        )

        existing = (
            await self.redis.get(
                redis_key
            )
        )

        # Another driver already accepted

        if existing:
            return False

        # =================================================
        # SAVE ACCEPTED DRIVER
        # =================================================

        await self.redis.set(
            redis_key,
            str(driver_id),
            ex=300
        )

        # =================================================
        # UPDATE TRIP
        # =================================================

        result = await self.db.execute(
            select(Trip).where(
                Trip.id == trip_id
            )
        )

        trip = (
            result.scalars().first()
        )

        if trip:

            trip.driver_id = driver_id

            trip.status = (
                TripStatus.DRIVER_ASSIGNED
            )

            await self.db.commit()

        return True

    # =====================================================
    # REJECT RIDE
    # =====================================================

    async def reject_ride(
        self,
        trip_id: UUID,
        driver_id: UUID
    ):

        if self.redis:

            await self.redis.set(
                (
                    f"trip_rejected:"
                    f"{trip_id}:{driver_id}"
                ),
                "REJECTED",
                ex=300
            )

    # =====================================================
    # CANCEL OTHER REQUESTS
    # =====================================================

    async def cancel_other_requests(
        self,
        trip_id: UUID,
        accepted_driver_id: str
    ):

        payload = {

            "event":
            "RIDE_REQUEST_CANCELLED",

            "trip_id":
            str(trip_id)
        }

        if self.websocket_manager:

            await (
                self.websocket_manager
                .broadcast_excluding(
                    message=payload,
                    excluded_user_id=(
                        accepted_driver_id
                    )
                )
            )

    # =====================================================
    # MAIN MATCHING FLOW
    # =====================================================

    async def match_driver(
        self,
        trip_id: UUID,
        pickup_lat: float,
        pickup_lng: float,
        vehicle_category: str
    ) -> Optional[str]:

        # =================================================
        # STEP 1
        # FIND NEARBY DRIVERS
        # =================================================

        nearby_drivers = (
            await self.find_nearby_drivers(
                pickup_lat=pickup_lat,

                pickup_lng=pickup_lng,

                vehicle_category=(
                    vehicle_category
                )
            )
        )

        if not nearby_drivers:
            return None

        # =================================================
        # STEP 2
        # SEND REQUESTS
        # =================================================

        accepted_driver = (
            await self.send_ride_requests(
                trip_id=trip_id,
                drivers=nearby_drivers
            )
        )

        return accepted_driver