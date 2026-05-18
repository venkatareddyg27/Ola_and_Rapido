# =========================================================
# ENUMS
# =========================================================

from sqlalchemy import Enum 
from enum import Enum 


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


class TransactionStatus(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class WalletTransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class RefundStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PROCESSED = "PROCESSED"
    
class EscrowStatus(str, Enum):
    INITIATED = "INITIATED"
    HELD = "HELD"
    UNDER_REVIEW = "UNDER_REVIEW"
    RELEASED = "RELEASED"
    PARTIALLY_RELEASED = "PARTIALLY_RELEASED"
    FORFEITED = "FORFEITED"
    FAILED = "FAILED"


class EscrowTransactionType(str, Enum):
    HOLD = "HOLD"
    RELEASE = "RELEASE"
    REFUND = "REFUND"
    DEDUCTION = "DEDUCTION"



# -------------------------
# ENUMS
# -------------------------

class PackageType(str, Enum):
    document = "document"
    food = "food"
    electronics = "electronics"
    grocery = "grocery"
    medicine = "medicine"
    clothes = "clothes"
    others = "others"


class WeightTier(str,Enum):
    light = "light"
    medium = "medium"
    heavy = "heavy"


class ParcelStatus(str, Enum):
    pending_pickup = "pending_pickup"
    driver_assigned = "driver_assigned"
    picked_up = "picked_up"
    in_transit = "in_transit"
    delivered = "delivered"
    cancelled = "cancelled"

