import enum

class UserRole(str, enum.Enum):

    CUSTOMER = "customer"

    DRIVER = "driver"

    OWNER = "owner"

    ADMIN = "admin"

class UserStatus(str, enum.Enum):

    ACTIVE = "active"

    SUSPENDED = "suspended"

    PENDING = "pending"


class OTPPurpose(str, enum.Enum):

    LOGIN = "login"

    KYC = "kyc"

    TRIP = "trip"

class KYCDocType(str, enum.Enum):

    AADHAAR = "aadhaar"

    PAN = "pan"

    DL = "dl"

    RC = "rc"

    INSURANCE = "insurance"

    PUC = "puc"


class KYCStatus(str, enum.Enum):

    PENDING = "pending"

    APPROVED = "approved"

    REJECTED = "rejected"


class SubscriptionPlan(str, enum.Enum):

    BASIC = "basic"

    PRO = "pro"


class DriverStatus(str, enum.Enum):

    OFFLINE = "offline"

    INACTIVE = "inactive"

    ACTIVE = "active"

    ONLINE = "online"

    ON_TRIP = "on_trip"

    BREAK = "break"
    BLOCKED = "BLOCKED"

    BLOCKED="blocked"


class DriverOnTripStatus(str, enum.Enum):

    AVAILABLE = "available"

    ON_TRIP = "on_trip"

    OFFLINE = "offline"


class VehicleCategory(str, enum.Enum):

    HATCHBACK = "hatchback"

    SEDAN = "sedan"

    SUV = "suv"

    LUXURY = "luxury"

    BIKE = "bike"

    AUTO = "auto"


class VehicleStatus(str, enum.Enum):

    PENDING = "pending"

    ACTIVE = "active"

    PAUSED = "paused"

    REJECTED = "rejected"


class VehiclePhotoAngle(str, enum.Enum):

    FRONT = "front"

    REAR = "rear"

    LEFT = "left"

    RIGHT = "right"

    INTERIOR = "interior"

    DASHBOARD = "dashboard"


class ServiceType(str, enum.Enum):

    BIKE = "bike"

    AUTO = "auto"

    MINI = "mini"

    SEDAN = "sedan"

    SUV = "suv"

    PARCEL = "parcel"

    RENTAL = "rental"


class TripStatus(str, enum.Enum):

    SEARCHING_DRIVER = "searching_driver"

    DRIVER_ASSIGNED = "driver_assigned"

    DRIVER_ARRIVED = "driver_arrived"

    IN_PROGRESS = "in_progress"

    COMPLETED = "completed"

    CANCELLED = "cancelled"

    NO_DRIVER_FOUND = "no_driver_found"


class PackageType(str, enum.Enum):

    DOCUMENT = "document"

    SMALL = "small"

    LARGE = "large"

    FOOD = "food"


class RentalStatus(str, enum.Enum):

    REQUESTED = "requested"

    ACCEPTED = "accepted"

    INSPECTION = "inspection"

    ACTIVE = "active"

    RETURNED = "returned"

    DISPUTED = "disputed"

    CANCELLED = "cancelled"


class DepositStatus(str, enum.Enum):

    HELD = "held"

    RELEASED = "released"

    PARTIALLY_DEDUCTED = (
        "partially_deducted"
    )

    FORFEITED = "forfeited"


class InspectionType(str, enum.Enum):

    PRE = "pre"

    POST = "post"


class PaymentMethod(str, enum.Enum):

    UPI = "upi"

    CARD = "card"

    WALLET = "wallet"

    CASH = "cash"

    NETBANKING = "netbanking"


class PaymentStatus(str, enum.Enum):

    PENDING = "pending"

    SUCCESS = "success"

    FAILED = "failed"

    REFUNDED = "refunded"


class WalletTransactionType(str, enum.Enum):

    CREDIT = "credit"

    DEBIT = "debit"


class PayoutMethod(str, enum.Enum):

    UPI = "upi"

    BANK = "bank"


class PayoutStatus(str, enum.Enum):

    PENDING = "pending"

    PROCESSED = "processed"

    FAILED = "failed"


class DisputeCategory(str, enum.Enum):

    FARE = "fare"

    DAMAGE = "damage"

    BEHAVIOUR = "behaviour"

    PAYMENT = "payment"

    DELIVERY = "delivery"

    OTHER = "other"


class DisputeStatus(str, enum.Enum):

    OPEN = "open"

    IN_REVIEW = "in_review"

    RESOLVED = "resolved"

    ESCALATED = "escalated"


class DisputePriority(str, enum.Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


class DiscountType(str, enum.Enum):

    FLAT = "flat"

    PERCENT = "percent"


class OTPPurposeEnum(str, enum.Enum):

    LOGIN = "login"

    REGISTER = "register"

    PHONE_VERIFICATION = (
        "phone_verification"
    )

    EMAIL_VERIFICATION = (
        "email_verification"
    )

    PASSWORD_RESET = (
        "password_reset"
    )

    TRIP_START = "trip_start"

    TRIP_END = "trip_end"

    PARCEL_PICKUP = (
        "parcel_pickup"
    )

    PARCEL_DELIVERY = (
        "parcel_delivery"
    )

    ACCOUNT_DELETE = (
        "account_delete"
    )


class ParcelStatus(str, enum.Enum):

    CREATED = "created"

    REQUESTED = "requested"

    DRIVER_ASSIGNED = (
        "driver_assigned"
    )

    ACCEPTED = "accepted"

    PICKUP_STARTED = (
        "pickup_started"
    )

    PICKED_UP = "picked_up"

    IN_TRANSIT = "in_transit"

    DELIVERED = "delivered"

    CANCELLED = "cancelled"

    FAILED = "failed"


class ParcelType(str, enum.Enum):

    PACKAGE = "package"

    DOCUMENT = "document"

    SMALL = "small"

    LARGE = "large"

    FOOD = "food"


class ParcelPriority(str, enum.Enum):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"

    URGENT = "urgent"


class ProofType(str, enum.Enum):

    PICKUP_PHOTO = "pickup_photo"

    DELIVERY_PHOTO = (
        "delivery_photo"
    )

    OTP = "otp"

    SIGNATURE = "signature"


class DeliveryAttemptStatus(str,enum.Enum):

    SUCCESS = "success"

    FAILED = "failed"

    RETRY = "retry"


class FeedbackType(str, enum.Enum):

    DRIVER = "driver"

    CUSTOMER = "customer"

    DELIVERY = "delivery"

    PAYMENT = "payment"

    APP = "app"

    OTHER = "other"