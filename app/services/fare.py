# =========================================================
# FILE: app/services/fare.py
# =========================================================

from app.core.enums import VehicleCategory


class FareCalculatorService:

    # =====================================================
    # VEHICLE CATEGORY PRICING
    # =====================================================

    VEHICLE_PRICING = {
        VehicleCategory.BIKE: {
            "base_fare": 30,
            "per_km_rate": 8
        },

        VehicleCategory.AUTO: {
            "base_fare": 50,
            "per_km_rate": 12
        },

        VehicleCategory.HATCHBACK: {
            "base_fare": 80,
            "per_km_rate": 15
        },

        VehicleCategory.SEDAN: {
            "base_fare": 100,
            "per_km_rate": 18
        },

        VehicleCategory.SUV: {
            "base_fare": 150,
            "per_km_rate": 22
        },

        VehicleCategory.LUXURY: {
            "base_fare": 300,
            "per_km_rate": 40
        }
    }

    # =====================================================
    # CALCULATE FARE
    # =====================================================

    @classmethod
    def calculate_fare(
        cls,
        vehicle_category: VehicleCategory,
        distance_km: float,
        surge_multiplier: float = 1.0
    ) -> float:

        # =================================================
        # VALIDATE VEHICLE CATEGORY
        # =================================================

        if vehicle_category not in cls.VEHICLE_PRICING:
            raise ValueError("Invalid vehicle category")

        # =================================================
        # GET PRICING
        # =================================================

        pricing = cls.VEHICLE_PRICING[vehicle_category]

        base_fare = pricing["base_fare"]

        per_km_rate = pricing["per_km_rate"]

        # =================================================
        # CALCULATE TOTAL FARE
        # =================================================

        total_fare = (
            base_fare +
            (distance_km * per_km_rate)
        ) * surge_multiplier

        # =================================================
        # RETURN ROUNDED FARE
        # =================================================

        return round(total_fare, 2)