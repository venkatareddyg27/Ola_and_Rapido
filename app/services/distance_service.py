from math import (radians,sin,cos,sqrt,atan2)


class DistanceService:

    EARTH_RADIUS_KM = 6371


    @classmethod
    def calculate_distance(

        cls,

        pickup_lat: float,
        pickup_lng: float,

        drop_lat: float,
        drop_lng: float) -> float:

        lat1 = radians(pickup_lat)

        lon1 = radians(pickup_lng)

        lat2 = radians(drop_lat)

        lon2 = radians(drop_lng)

        dlat = lat2 - lat1

        dlon = lon2 - lon1

        a = (

            sin(dlat / 2) ** 2

            +                                  # HAVERSINE FORMULA

            cos(lat1) *
            cos(lat2) *

            sin(dlon / 2) ** 2
        )

        c = (
            2 *
            atan2(
                sqrt(a),
                sqrt(1 - a)
            ))

        distance = (
            cls.EARTH_RADIUS_KM * c)

        return round(distance, 2)

    @classmethod
    def estimate_duration(

        cls,

        distance_km: float,

        average_speed_kmph: float = 35) -> int:


        if average_speed_kmph <= 0:

            return 0

        duration_hours = (
            distance_km /
            average_speed_kmph)

        duration_minutes = (
            duration_hours * 60)

        return round(duration_minutes)


    @classmethod
    def is_serviceable_distance(

        cls,

        distance_km: float,

        max_distance_km: float = 100) -> bool:

        return (
            distance_km <=
            max_distance_km)