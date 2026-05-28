from decimal import Decimal

from app.core.enums import ParcelPriority, VehicleCategory

from app.utils.fare_config import (
    BASE_FARES,
    PER_KM_RATE,
    PER_MINUTE_RATE,
    BOOKING_FEE,
    GST_PERCENTAGE,
    MAX_SURGE_MULTIPLIER,
    SURGE_THRESHOLDS,
)
class FareCalculatorService:

    @staticmethod
    def calculate_surge_multiplier(active_requests: int, active_drivers: int) -> Decimal:
        if active_drivers <= 0:
            return MAX_SURGE_MULTIPLIER

        demand_ratio = active_requests / active_drivers

        if demand_ratio <= 1:
            return SURGE_THRESHOLDS[1]
        elif demand_ratio <= 2:
            return SURGE_THRESHOLDS[2]
        elif demand_ratio <= 3:
            return SURGE_THRESHOLDS[3]
        elif demand_ratio <= 5:
            return SURGE_THRESHOLDS[5]

        return MAX_SURGE_MULTIPLIER

    @staticmethod
    def calculate_tax(amount: Decimal) -> Decimal:
        tax = (amount * GST_PERCENTAGE) / Decimal("100")
        return tax.quantize(Decimal("0.01"))

    @staticmethod
    def calculate_fare(
        vehicle_category: str,
        distance_km: float,
        duration_minutes: int,
        active_requests: int = 10,
        active_drivers: int = 10
    ):
        vehicle_category = vehicle_category.lower()

        base_fare = BASE_FARES.get(vehicle_category, Decimal("50"))
        distance_rate = PER_KM_RATE.get(vehicle_category, Decimal("10"))
        time_rate = PER_MINUTE_RATE.get(vehicle_category, Decimal("2"))

        distance_fare = Decimal(str(distance_km)) * distance_rate
        time_fare = Decimal(str(duration_minutes)) * time_rate

        subtotal = base_fare + distance_fare + time_fare + BOOKING_FEE

        surge_multiplier = FareCalculatorService.calculate_surge_multiplier(
            active_requests=active_requests,
            active_drivers=active_drivers
        )

        surge_amount = subtotal * (surge_multiplier - Decimal("1.0"))
        surged_total = subtotal + surge_amount

        tax_amount = FareCalculatorService.calculate_tax(surged_total)

        final_fare = (surged_total + tax_amount).quantize(Decimal("0.01"))

        return {
            "vehicle_category": vehicle_category,
            "base_fare": float(base_fare),
            "distance_fare": float(distance_fare),
            "time_fare": float(time_fare),
            "booking_fee": float(BOOKING_FEE),
            "subtotal": float(subtotal),
            "surge_multiplier": float(surge_multiplier),
            "surge_amount": float(surge_amount),
            "tax_amount": float(tax_amount),
            "total_fare": float(final_fare),
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

        surge_amount = Decimal("0.00")

        total_charge = base_fare + distance_price + weight_price + priority_fee + surge_amount

        tax_amount = FareCalculatorService.calculate_tax(total_charge)
        final_fare = (total_charge + tax_amount).quantize(Decimal("0.01"))

        return {
            "total_charge": float(total_charge),
            "surge_amount": float(surge_amount),
            "tax_amount": float(tax_amount),
            "total_fare": float(final_fare),
        }