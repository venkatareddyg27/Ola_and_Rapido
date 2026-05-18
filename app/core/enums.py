# =========================================================
# ENUMS
# =========================================================

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




class UserTypeEnum(str, Enum):
    driver = "driver"
    customer = "customer"
class ActionTypeEnum(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"
    ban = "ban"
    unban = "unban"
    refund = "refund"
    escalate = "escalate"
    resolve = "resolve"
    assign = "assign"
    export = "export"

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    DRIVER = "DRIVER"
    STORE_MANAGER = "STORE_MANAGER"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    
class KYCStatus(str, Enum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class LoyaltyTier(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    
class DriverStatus(str, Enum):
    IDLE = "idle"
    ON_RIDE = "on_ride"
    ON_DELIVERY = "on_delivery"
    OFFLINE = "offline"
    BREAK = "break"
    
class FuelType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    CNG = "cng"
    EV = "ev"
    HYBRID = "hybrid"


class TransmissionType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class VehicleVerificationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"