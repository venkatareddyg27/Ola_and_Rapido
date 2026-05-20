# enums.py

import enum


# =========================================================
# USER & AUTHENTICATION ENUMS
# =========================================================

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    DRIVER   = "driver"
    OWNER    = "owner"
    ADMIN    = "admin"


class UserStatus(str, enum.Enum):
    ACTIVE    = "active"
    SUSPENDED = "suspended"
    PENDING   = "pending"


class OTPPurpose(str, enum.Enum):
    LOGIN = "login"
    KYC   = "kyc"
    TRIP  = "trip"


# =========================================================
# KYC & DOCUMENT ENUMS
# =========================================================

class KYCDocType(str, enum.Enum):
    AADHAAR   = "aadhaar"
    PAN       = "pan"
    DL        = "dl"
    RC        = "rc"
    INSURANCE = "insurance"
    PUC       = "puc"


class KYCStatus(str, enum.Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# =========================================================
# DRIVER & VEHICLE ENUMS
# =========================================================

class SubscriptionPlan(str, enum.Enum):
    BASIC = "basic"
    PRO   = "pro"


class DriverStatus(str, enum.Enum):
    OFFLINE = "offline"
    ONLINE  = "online"
    ON_TRIP = "on_trip"
    BREAK   = "break"
class DriverOnTripStatus(str, enum.Enum):

    AVAILABLE = "available"

    ON_TRIP = "on_trip"

    OFFLINE = "offline"

class VehicleCategory(str, enum.Enum):
    HATCHBACK = "hatchback"
    SEDAN     = "sedan"
    SUV       = "suv"
    LUXURY    = "luxury"
    BIKE      = "bike"
    AUTO      = "auto"


class VehicleStatus(str, enum.Enum):
    PENDING  = "pending"
    ACTIVE   = "active"
    PAUSED   = "paused"
    REJECTED = "rejected"


class VehiclePhotoAngle(str, enum.Enum):
    FRONT     = "front"
    REAR      = "rear"
    LEFT      = "left"
    RIGHT     = "right"
    INTERIOR  = "interior"
    DASHBOARD = "dashboard"


# =========================================================
# TRIP & SERVICE ENUMS
# =========================================================

class ServiceType(str, enum.Enum):
    BIKE    = "bike"
    AUTO    = "auto"
    MINI    = "mini"
    SEDAN   = "sedan"
    SUV     = "suv"
    PARCEL  = "parcel"
    RENTAL  = "rental"


class TripStatus(str, enum.Enum):
    SEARCHING       = "searching"
    DRIVER_ASSIGNED = "driver_assigned"   # added — used by matching.py
    ACCEPTED        = "accepted"
    ARRIVED         = "arrived"
    STARTED         = "started"
    COMPLETED       = "completed"
    CANCELLED       = "cancelled"


class PackageType(str, enum.Enum):
    DOCUMENT = "document"
    SMALL    = "small"
    LARGE    = "large"
    FOOD     = "food"


# =========================================================
# RENTAL ENUMS
# =========================================================

class RentalStatus(str, enum.Enum):
    REQUESTED  = "requested"
    ACCEPTED   = "accepted"
    INSPECTION = "inspection"
    ACTIVE     = "active"
    RETURNED   = "returned"
    DISPUTED   = "disputed"
    CANCELLED  = "cancelled"


class DepositStatus(str, enum.Enum):
    HELD                = "held"
    RELEASED            = "released"
    PARTIALLY_DEDUCTED  = "partially_deducted"
    FORFEITED           = "forfeited"


class InspectionType(str, enum.Enum):
    PRE  = "pre"
    POST = "post"


# =========================================================
# PAYMENT ENUMS
# =========================================================

class PaymentMethod(str, enum.Enum):
    UPI        = "upi"
    CARD       = "card"
    WALLET     = "wallet"
    CASH       = "cash"
    NETBANKING = "netbanking"


class PaymentStatus(str, enum.Enum):
    PENDING  = "pending"
    SUCCESS  = "success"
    FAILED   = "failed"
    REFUNDED = "refunded"


class WalletTransactionType(str, enum.Enum):
    CREDIT = "credit"
    DEBIT  = "debit"


class PayoutMethod(str, enum.Enum):
    UPI  = "upi"
    BANK = "bank"


class PayoutStatus(str, enum.Enum):
    PENDING   = "pending"
    PROCESSED = "processed"
    FAILED    = "failed"


# =========================================================
# SUPPORT & OPERATIONS ENUMS
# =========================================================

class DisputeCategory(str, enum.Enum):
    FARE      = "fare"
    DAMAGE    = "damage"
    BEHAVIOUR = "behaviour"
    PAYMENT   = "payment"
    DELIVERY  = "delivery"
    OTHER     = "other"


class DisputeStatus(str, enum.Enum):
    OPEN       = "open"
    IN_REVIEW  = "in_review"
    RESOLVED   = "resolved"
    ESCALATED  = "escalated"


class DisputePriority(str, enum.Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


class DiscountType(str, enum.Enum):
    FLAT    = "flat"
    PERCENT = "percent"