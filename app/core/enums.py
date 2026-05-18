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

# =========================================================
# DOCUMENT TYPES
# =========================================================

class DocumentType(str, Enum):
    aadhaar = "aadhaar"
    pan = "pan"
    driving_license = "driving_license"
    rc = "rc"
    insurance = "insurance"
    puc = "puc"
    selfie = "selfie"


# =========================================================
# AADHAAR EKYC STATUS
# =========================================================

class AadhaarEkycStatus(str, Enum):
    otp_sent = "otp_sent"
    otp_verified = "otp_verified"
    completed = "completed"
    failed = "failed"

    

class RentalBookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class DamageClaimStatus(str, Enum):
    NONE = "none"
    RAISED = "raised"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SETTLED = "settled"

class RideType(str, Enum):
    BIKE = "bike"
    AUTO = "auto"
    CAB = "cab"
    RENTAL = "rental"


class RideStatus(str, Enum):
    SEARCHING = "searching"
    DRIVER_ASSIGNED = "driver_assigned"
    DRIVER_ARRIVED = "driver_arrived"
    OTP_VERIFIED = "otp_verified"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PaymentMethod(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"
    WALLET = "wallet"
