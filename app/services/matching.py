
import asyncio

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
    TripStatus,
    VehicleCategory
)

from app.services.distance_service import (
    DistanceService
)

# =========================================================
# CONFIG
# =========================================================

DEFAULT_RADIUS_KM = 5

MAX_DRIVER_REQUESTS = 3

REQUEST_TIMEOUT = 30

RADIUS_EXPANSION_STEPS = [
    5,
    10,
    15
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
            111.0 *
            max(0.1, abs(lat))
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
        # LATEST DRIVER LOCATION SUBQUERY
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
        # QUERY DRIVERS
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

                Vehicle.category ==
                VehicleCategory(
                    vehicle_category
                ),

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

        # =================================================
        # DISTANCE FILTER
        # =================================================

        for (
            driver,
            user,
            vehicle,
            location
        ) in rows:

            # =============================================
            # SKIP REJECTED DRIVERS
            # =============================================

            if self.redis:

                rejected = await self.redis.get(
                    f"trip_rejected:{user.id}"
                )

                if rejected:
                    continue

            # =============================================
            # CALCULATE DISTANCE
            # =============================================

            distance = (
                DistanceService
                .calculate_distance(

                    pickup_lat,
                    pickup_lng,

                    float(location.latitude),
                    float(location.longitude)
                )
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
        # SORT BY SCORE
        # =================================================

        matched_drivers.sort(
            key=lambda x: x["score"]
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

        # =================================================
        # GET TRIP
        # =================================================

        trip_result = await self.db.execute(

            select(Trip).where(
                Trip.id == trip_id
            )
        )

        trip = trip_result.scalars().first()

        if not trip:
            return None

        # =================================================
        # SELECT DRIVERS
        # =================================================

        selected_drivers = (
            drivers[:MAX_DRIVER_REQUESTS]
        )

        notified_user_ids = [

            d["user_id"]

            for d in selected_drivers
        ]

        # =================================================
        # REDIS MATCH STATE
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
                str(trip.id),

                "pickup_address":
                trip.pickup_address,

                "drop_address":
                trip.drop_address,

                "pickup_distance_km":
                driver["distance"],

                "estimated_fare":
                float(
                    trip.estimated_fare
                ),

                "vehicle_category":
                trip.vehicle_category.value
            }

            if self.websocket_manager:

                await (
                    self.websocket_manager
                    .send_to_user(

                        user_id=
                        driver["user_id"],

                        message=
                        payload
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

            await self.cancel_other_requests(

                trip_id=trip_id,

                accepted_driver_id=
                accepted_driver,

                notified_user_ids=
                notified_user_ids
            )

        return accepted_driver

    # =====================================================
    # WAIT FOR ACCEPTANCE
    # =====================================================

    async def wait_for_acceptance(

        self,

        trip_id: UUID

    ) -> Optional[str]:

        channel = (
            f"trip_accept_ch:{trip_id}"
        )

        if self.redis:

            result = await self.redis.blpop(
                channel,
                timeout=REQUEST_TIMEOUT
            )

            if result:

                _, value = result

                return (

                    value.decode()

                    if isinstance(
                        value,
                        bytes
                    )

                    else value
                )

            return None

        # =================================================
        # FALLBACK POLLING
        # =================================================

        for _ in range(
            REQUEST_TIMEOUT
        ):

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

        if not self.redis:

            raise RuntimeError(
                "Redis required"
            )

        redis_key = (
            f"trip_accepted:{trip_id}"
        )

        accept_channel = (
            f"trip_accept_ch:{trip_id}"
        )

        # =================================================
        # LOCK ACCEPTANCE
        # =================================================

        claimed = await self.redis.set(

            redis_key,

            str(driver_id),

            ex=300,

            nx=True
        )

        if not claimed:
            return False

        # =================================================
        # GET TRIP
        # =================================================

        result = await self.db.execute(

            select(Trip).where(
                Trip.id == trip_id
            )
        )

        trip = result.scalars().first()

        if not trip:

            await self.redis.delete(
                redis_key
            )

            return False

        # =================================================
        # VALIDATE STATUS
        # =================================================

        if trip.status != (
            TripStatus.SEARCHING_DRIVER
        ):

            return False

        # =================================================
        # ASSIGN DRIVER
        # =================================================

        trip.driver_id = driver_id

        trip.status = (
            TripStatus.DRIVER_ASSIGNED
        )

        # =================================================
        # UPDATE DRIVER STATUS
        # =================================================

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

        # =================================================
        # COMMIT
        # =================================================

        try:

            await self.db.commit()

        except Exception:

            await self.db.rollback()

            raise

        # =================================================
        # NOTIFY ACCEPTANCE
        # =================================================

        await self.redis.lpush(
            accept_channel,
            str(driver_id)
        )

        await self.redis.expire(
            accept_channel,
            60
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

        if self.redis:

            await self.redis.set(

                f"trip_rejected:{driver_id}",

                "REJECTED",

                ex=300
            )

    # =====================================================
    # CANCEL OTHER REQUESTS
    # =====================================================

    async def cancel_other_requests(

        self,

        trip_id: UUID,

        accepted_driver_id: str,

        notified_user_ids: List[str]

    ):

        if not self.websocket_manager:
            return

        payload = {

            "event":
            "RIDE_REQUEST_CANCELLED",

            "trip_id":
            str(trip_id)
        }

        for user_id in notified_user_ids:

            if user_id == accepted_driver_id:
                continue

            await (
                self.websocket_manager
                .send_to_user(

                    user_id=user_id,

                    message=payload
                )
            )

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

        for radius_km in (
            RADIUS_EXPANSION_STEPS
        ):

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

            # =============================================
            # NO DRIVERS
            # =============================================

            if not nearby_drivers:
                continue

            # =============================================
            # SEND REQUESTS
            # =============================================

            accepted_driver = (

                await self
                .send_ride_requests(

                    trip_id=trip_id,

                    drivers=
                    nearby_drivers
                )
            )

            # =============================================
            # DRIVER ACCEPTED
            # =============================================

            if accepted_driver:
                return accepted_driver

        return None