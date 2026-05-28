from decimal import Decimal

BASE_FARES = {

    "bike": Decimal("40"),

    "auto": Decimal("60"),

    "car": Decimal("100")
}

PER_KM_RATE = {

    "bike": Decimal("8"),

    "auto": Decimal("12"),

    "car": Decimal("18")
}

PER_MINUTE_RATE = {

    "bike": Decimal("1"),

    "auto": Decimal("2"),

    "car": Decimal("3")
}


BOOKING_FEE = Decimal("10")


GST_PERCENTAGE = Decimal("5")

MAX_SURGE_MULTIPLIER = Decimal("3.0")

SURGE_THRESHOLDS = {

    1: Decimal("1.0"),

    2: Decimal("1.2"),

    3: Decimal("1.5"),

    5: Decimal("2.0")
}