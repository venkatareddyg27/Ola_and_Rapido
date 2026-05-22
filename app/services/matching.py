import asyncio

from math import (
    cos,
    radians
)

from uuid import UUID

from typing import (
    List,
    Dict,
    Optional
)

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.user_models import (
    DriverProfile,
    User,
    DriverLocation
)

from app.models.vehicles import (
    Vehicle
)

from app.models.trips import (
    Trip
)

from app.core.enums import (
    DriverStatus,
    TripStatus
)

from app.services.distance_service import (
    DistanceService
)

# =========================================================
# CONFIG
# =========================================================

DEFAULT_RADIUS_KM = 5

MAX_DRIVER_REQUESTS = 3

RADIUS_EXPANSION_STEPS = [
    5,
    10,
    15,
    20
]

RATING_WEIGHT = 0.3

# =========================================================
# DRIVER SCORE
# =========================================================

def driver_score(
    distance: float,
    rating: float,
    radius_km: float
) -> float:

    normalized_distance = (
        distance / radius_km
    )

    normalized_rating = (
        1.0 - (rating / 5.0)
    )

    return (
        (
            1 - RATING_WEIGHT
        ) * normalized_distance
    ) + (
        RATING_WEIGHT *
        normalized_rating
    )

# =========================================================
# BOUNDING BOX
# =========================================================

def bounding_box(
    lat: float,
    lng: float,
    radius_km: float
):

    lat_delta = (
        radius_km / 111.0
    )

    lng_delta = (

        radius_km /

        (
            111.320 *
            cos(
                radians(lat)
            )
        )
    )

    return (

        lat - lat_delta,

        lat + lat_delta,

        lng - lng_delta,

        lng + lng_delta
    )

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

    # =====================================================
    # FIND NEARBY DRIVERS
    # =====================================================

    async def find_nearby_drivers(

        self,

        pickup_lat: float,

        pickup_lng: float,

        vehicle_category: str,

        radius_km: int = DEFAULT_RADIUS_KM

    ) -> List[Dict]:

        matched_drivers = []

        min_lat, max_lat, min_lng, max_lng = (

            bounding_box(
                pickup_lat,
                pickup_lng,
                radius_km
            )
        )

        # =================================================
        # LATEST LOCATION SUBQUERY
        # =================================================

        latest_location_subquery = (

            select(DriverLocation.id)

            .where(
                DriverLocation.driver_id ==
                DriverProfile.id
            )

            .order_by(
                DriverLocation.updated_at.desc()
            )

            .limit(1)

            .correlate(DriverProfile)

            .scalar_subquery()
        )

        # =================================================
        # QUERY
        # =================================================

        result = await self.db.execute(

            select(
                DriverProfile,
                User,
                Vehicle,
                DriverLocation
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

            .join(
                DriverLocation,
                DriverLocation.id ==
                latest_location_subquery
            )

            .where(

                DriverProfile.status ==
                DriverStatus.ONLINE,

                DriverProfile.is_verified == True,

                DriverLocation.is_active == True,

                Vehicle.category ==
                vehicle_category.upper(),

                DriverLocation.latitude.between(
                    min_lat,
                    max_lat
                ),

                DriverLocation.longitude.between(
                    min_lng,
                    max_lng
                )
            )
        )

        rows = result.all()

        print(
            f"Found {len(rows)} nearby drivers"
        )

        # =================================================
        # FILTER DISTANCE
        # =================================================

        for (
            driver,
            user,
            vehicle,
            location
        ) in rows:

            distance = (

                DistanceService
                .calculate_distance(

                    pickup_lat,
                    pickup_lng,

                    float(location.latitude),
                    float(location.longitude)
                )
            )

            print(
                f"Driver {driver.id} distance: {distance}"
            )

            if distance > radius_km:
                continue

            rating = float(
                driver.rating or 5
            )

            matched_drivers.append({

                "driver_id":
                str(driver.id),

                "user_id":
                str(user.id),

                "vehicle_id":
                str(vehicle.id),

                "distance":
                round(distance, 2),

                "rating":
                rating,

                "total_trips":
                driver.total_trips,

                "latitude":
                float(location.latitude),

                "longitude":
                float(location.longitude),

                "score":
                driver_score(
                    distance,
                    rating,
                    radius_km
                )
            })

        # =================================================
        # SORT
        # =================================================

        matched_drivers.sort(
            key=lambda x: x["score"]
        )

        print(
            f"Matched Drivers: {matched_drivers}"
        )

        return matched_drivers

    # =====================================================
    # AUTO ASSIGN DRIVER
    # =====================================================

    async def send_ride_requests(

        self,

        trip_id: UUID,

        drivers: List[Dict]

    ) -> Optional[str]:

        if not drivers:
            return None

        # =================================================
        # AUTO ASSIGN FIRST DRIVER
        # =================================================

        first_driver = drivers[0]

        print(
            f"Auto assigned driver: {first_driver['driver_id']}"
        )

        return first_driver["driver_id"]

    # =====================================================
    # ACCEPT RIDE
    # =====================================================

    async def accept_ride(

        self,

        trip_id: UUID,

        driver_id: UUID

    ) -> bool:

        result = await self.db.execute(

            select(Trip).where(
                Trip.id == trip_id
            )
        )

        trip = result.scalars().first()

        if not trip:
            return False

        if trip.driver_id:
            return False

        trip.driver_id = driver_id

        trip.status = (
            TripStatus.DRIVER_ASSIGNED
        )

        driver_result = await self.db.execute(

            select(DriverProfile).where(
                DriverProfile.id ==
                driver_id
            )
        )

        driver_profile = (
            driver_result.scalars().first()
        )

        if driver_profile:

            driver_profile.status = (
                DriverStatus.ON_TRIP
            )

        await self.db.commit()

        print(
            f"Trip assigned to driver {driver_id}"
        )

        return True

    # =====================================================
    # REJECT RIDE
    # =====================================================

    async def reject_ride(

        self,

        trip_id: UUID,

        driver_id: UUID

    ):

        print(
            f"Driver rejected trip: {driver_id}"
        )

        return True

    # =====================================================
    # MATCH DRIVER
    # =====================================================

    async def match_driver(

        self,

        trip_id: UUID,

        pickup_lat: float,

        pickup_lng: float,

        vehicle_category: str

    ) -> Optional[str]:

        print(
            f"Searching drivers for {vehicle_category}"
        )

        for radius_km in (
            RADIUS_EXPANSION_STEPS
        ):

            print(
                f"Searching in radius {radius_km} KM"
            )

            nearby_drivers = (

                await self
                .find_nearby_drivers(

                    pickup_lat=
                    pickup_lat,

                    pickup_lng=
                    pickup_lng,

                    vehicle_category=
                    vehicle_category,

                    radius_km=
                    radius_km
                )
            )

            if not nearby_drivers:

                print(
                    f"No drivers in {radius_km} KM"
                )

                continue

            accepted_driver = (

                await self
                .send_ride_requests(

                    trip_id=trip_id,

                    drivers=
                    nearby_drivers
                )
            )

            if accepted_driver:

                # =========================================
                # AUTO ASSIGN TRIP
                # =========================================

                await self.accept_ride(

                    trip_id=trip_id,

                    driver_id=UUID(
                        accepted_driver
                    )
                )

                return accepted_driver

        print("No driver accepted ride")

        return None