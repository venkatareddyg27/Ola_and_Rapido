import enum

class UserRole(str, enum.Enum):
    RENTER = "RENTER"
    DRIVER = "DRIVER"
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

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

class DriverOnTripStatus(str, enum.Enum):
    AVAILABLE = "available"
    ON_TRIP = "on_trip"
    OFFLINE = "offline"

class VehicleCategory(str, enum.Enum):
    HATCHBACK = "HATCHBACK"
    SEDAN = "SEDAN"
    SUV = "SUV"
    LUXURY = "LUXURY"
    BIKE = "BIKE"
    AUTO = "AUTO"
    CAR = "CAR"

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
    BIKE = "BIKE"
    AUTO = "AUTO"
    MINI = "MINI"
    SEDAN = "SEDAN"
    SUV = "SUV"
    PARCEL = "PARCEL"
    RENTAL = "RENTAL"

class TripStatus(str, enum.Enum):
    PENDING_CONFIRMATION = "PENDING"
    SEARCHING_DRIVER = "SEARCHING_DRIVER"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    DRIVER_ARRIVED = "DRIVER_ARRIVED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_DRIVER_FOUND = "NO_DRIVER_FOUND"

class PackageType(str, enum.Enum):
    DOCUMENT = "document"
    SMALL = "small"
    LARGE = "large"
    FOOD = "food"

class RentalStatus(str, enum.Enum):
    REQUESTED = "requested"
    COMPLETED = "completed"
    ACCEPTED = "accepted"
    INSPECTION = "inspection"
    ACTIVE = "active"
    RETURNED = "returned"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"

class DepositStatus(str, enum.Enum):
    HELD = "held"
    RELEASED = "released"
    PARTIALLY_DEDUCTED = "partially_deducted"
    FORFEITED = "forfeited"
    REFUNDED = "refunded"

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
    PHONE_VERIFICATION = "phone_verification"
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    TRIP_START = "trip_start"
    TRIP_END = "trip_end"
    PARCEL_PICKUP = "parcel_pickup"
    PARCEL_DELIVERY = "parcel_delivery"
    ACCOUNT_DELETE = "account_delete"

class ParcelStatus(str, enum.Enum):
    PENDING_CONFIRMATION = "PENDING_CONFIRMATION"
    PENDING = "PENDING"
    CREATED = "CREATED"
    REQUESTED = "REQUESTED"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    ACCEPTED = "ACCEPTED"
    PICKUP_STARTED = "PICKUP_STARTED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class ParcelType(str, enum.Enum):
    PACKAGE = "PACKAGE"
    DOCUMENT = "DOCUMENT"
    SMALL = "SMALL"
    LARGE = "LARGE"
    FOOD = "FOOD"

class ParcelPriority(str, enum.Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

class ProofType(str, enum.Enum):
    PICKUP_PHOTO = "PICKUP_PHOTO"
    DELIVERY_PHOTO = "DELIVERY_PHOTO"
    OTP = "OTP"
    SIGNATURE = "SIGNATURE"

class DeliveryAttemptStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRY = "RETRY"

class FeedbackType(str, enum.Enum):
    DRIVER = "DRIVER"
    CUSTOMER = "CUSTOMER"
    DELIVERY = "DELIVERY"
    PAYMENT = "PAYMENT"
    APP = "APP"
    OTHER = "OTHER"
class DeductionType(str, enum.Enum):
    FARE = "fare"
    DAMAGE = "damage"
    BEHAVIOUR = "behaviour"
    PAYMENT = "payment"
    DELIVERY = "delivery"
    OTHER = "other"