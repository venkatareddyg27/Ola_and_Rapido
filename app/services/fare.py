from decimal import Decimal

from app.core.enums import ParcelPriority, VehicleCategory

from app.utils.fare_config import (
    VEHICLE_PRICING
)


class FareCalculatorService:

    # =====================================================
    # CALCULATE FARE
    # =====================================================

    @classmethod
    def calculate_fare(
        cls,
        vehicle_category: VehicleCategory,
        distance_km: float,
        surge_multiplier: float = 1.0,
        waiting_charge: float = 0,
        toll_charge: float = 0
    ) -> dict:

        # =================================================
        # VALIDATE CATEGORY
        # =================================================

        if vehicle_category not in VEHICLE_PRICING:

            raise ValueError(
                "Invalid vehicle category"
            )

        # =================================================
        # GET PRICING
        # =================================================

        pricing = VEHICLE_PRICING[
            vehicle_category
        ]

        base_fare = pricing["base_fare"]

        per_km_rate = pricing["per_km_rate"]

        minimum_fare = pricing[
            "minimum_fare"
        ]

        # =================================================
        # DISTANCE FARE
        # =================================================

        distance_fare = (
            distance_km *
            per_km_rate
        )

        # =================================================
        # TOTAL BEFORE SURGE
        # =================================================

        subtotal = (
            base_fare +
            distance_fare +
            waiting_charge +
            toll_charge
        )

        # =================================================
        # APPLY SURGE
        # =================================================

        total_fare = (
            subtotal *
            surge_multiplier
        )

        # =================================================
        # APPLY MINIMUM FARE
        # =================================================

        if total_fare < minimum_fare:

            total_fare = minimum_fare

        # =================================================
        # RETURN RESPONSE
        # =================================================

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

    # =====================================================
    # CALCULATE DELIVERY CHARGE
    # =====================================================

    @classmethod
    def calculate_delivery_charge(
        cls,
        distance_km: float,
        weight_kg: Decimal,
        priority: ParcelPriority,
    ) -> dict:

        base_fare = Decimal("35.00")
        per_km_charge = Decimal("10.00")
        weight_charge_per_kg = Decimal("5.00")

        distance_price = Decimal(str(round(distance_km, 2))) * per_km_charge
        weight_price = weight_kg * weight_charge_per_kg

        priority_fee = Decimal("0.00")

        if priority.value == "high":
            priority_fee = Decimal("30.00")
        elif priority.value == "urgent":
            priority_fee = Decimal("60.00")

        total_charge = base_fare + distance_price + weight_price + priority_fee

        return {
            "total_charge": total_charge
        }