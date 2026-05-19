
from enum import Enum
# =========================================================
# ENUMS
# =========================================================

class FuelType(str, Enum):
    PETROL = "PETROL"
    DIESEL = "DIESEL"
    CNG = "CNG"
    EV = "EV"
    HYBRID = "HYBRID"


class TransmissionType(str, Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"


class VehicleVerificationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VehicleType(str, Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    SCOOTER = "SCOOTER"



