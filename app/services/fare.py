from app.core.enums import VehicleCategory

from app.utils.fare_config import (VEHICLE_PRICING)


class FareCalculatorService:


    @classmethod
    def calculate_fare(
        cls,
        vehicle_category: VehicleCategory,
        distance_km: float,
        surge_multiplier: float = 1.0,
        waiting_charge: float = 0,
        toll_charge: float = 0) -> dict:


        if vehicle_category not in VEHICLE_PRICING:

            raise ValueError(
                "Invalid vehicle category")


        pricing = VEHICLE_PRICING[
            vehicle_category]

        base_fare = pricing["base_fare"]

        per_km_rate = pricing["per_km_rate"]

        minimum_fare = pricing[
            "minimum_fare"]

        distance_fare = (
            distance_km *
            per_km_rate)

        subtotal = (
            base_fare +
            distance_fare +
            waiting_charge +
            toll_charge)


        total_fare = (
            subtotal *
            surge_multiplier)

        if total_fare < minimum_fare:

            total_fare = minimum_fare

        return {

            "vehicle_category":
            vehicle_category.value,

            "distance_km":
            round(distance_km, 2),

            "base_fare":
            round(base_fare, 2),

            "distance_fare":
            round(distance_fare, 2),

            "waiting_charge":
            round(waiting_charge, 2),

            "toll_charge":
            round(toll_charge, 2),

            "surge_multiplier":
            surge_multiplier,

            "total_fare":
            round(total_fare, 2)
        }