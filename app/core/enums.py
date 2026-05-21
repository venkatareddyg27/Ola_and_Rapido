from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    STORE_MANAGER = "STORE_MANAGER"


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class DeviceTypeEnum(str, Enum):
    ANDROID = "ANDROID"
    IOS = "IOS"
    WEB = "WEB"


class OTPPurposeEnum(str, Enum):
    LOGIN = "LOGIN"
    REGISTER = "REGISTER"
    PASSWORD_RESET = "PASSWORD_RESET"
    MOBILE_VERIFICATION = "MOBILE_VERIFICATION"
    KYC = "KYC"
    TRIP = "TRIP"


class LoginStatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class BlockStatusEnum(str, Enum):
    TEMPORARY = "TEMPORARY"
    PERMANENT = "PERMANENT"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"
    PENDING = "pending"


class AccountStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"
    SUSPENDED = "SUSPENDED"


class TokenTypeEnum(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
    RESET = "RESET"


class PermissionEnum(str, Enum):
    CREATE_USER = "CREATE_USER"
    UPDATE_USER = "UPDATE_USER"
    DELETE_USER = "DELETE_USER"

    CREATE_DRIVER = "CREATE_DRIVER"
    UPDATE_DRIVER = "UPDATE_DRIVER"
    DELETE_DRIVER = "DELETE_DRIVER"

    CREATE_RIDE = "CREATE_RIDE"
    CANCEL_RIDE = "CANCEL_RIDE"
    COMPLETE_RIDE = "COMPLETE_RIDE"

    CREATE_PARCEL = "CREATE_PARCEL"
    UPDATE_PARCEL = "UPDATE_PARCEL"

    VIEW_REPORTS = "VIEW_REPORTS"
    MANAGE_PAYMENTS = "MANAGE_PAYMENTS"
    MANAGE_KYC = "MANAGE_KYC"
    MANAGE_DISPUTES = "MANAGE_DISPUTES"
    FULL_ADMIN_ACCESS = "FULL_ADMIN_ACCESS"


class RoleNameEnum(str, Enum):
    USER = "USER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    FINANCE_MANAGER = "FINANCE_MANAGER"


class PasswordResetStatusEnum(str, Enum):
    PENDING = "PENDING"
    USED = "USED"
    EXPIRED = "EXPIRED"


class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentMethodTypeEnum(str, Enum):
    CARD = "CARD"
    UPI = "UPI"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"
    CASH = "CASH"


class WalletTransactionTypeEnum(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class WalletRechargeStatusEnum(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentTransactionStatusEnum(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"


class RefundStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


class InvoiceStatusEnum(str, Enum):
    GENERATED = "GENERATED"
    SENT = "SENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class SettlementStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PaymentGatewayEnum(str, Enum):
    RAZORPAY = "RAZORPAY"
    STRIPE = "STRIPE"
    PAYTM = "PAYTM"
    PHONEPE = "PHONEPE"
    CASHFREE = "CASHFREE"


class CurrencyEnum(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"


class PaymentReferenceTypeEnum(str, Enum):
    RIDE = "RIDE"
    PARCEL = "PARCEL"
    RENTAL = "RENTAL"
    WALLET_RECHARGE = "WALLET_RECHARGE"
    ESCROW = "ESCROW"


class GatewayLogStatusEnum(str, Enum):
    REQUESTED = "REQUESTED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class TaxTypeEnum(str, Enum):
    CGST = "CGST"
    SGST = "SGST"
    IGST = "IGST"


class PaymentSourceEnum(str, Enum):
    MOBILE_APP = "MOBILE_APP"
    WEB_APP = "WEB_APP"
    ADMIN_PANEL = "ADMIN_PANEL"
    API = "API"


class EscrowStatusEnum(str, Enum):
    INITIATED = "INITIATED"
    HELD = "HELD"
    PARTIALLY_RELEASED = "PARTIALLY_RELEASED"
    RELEASED = "RELEASED"
    REFUNDED = "REFUNDED"
    FORFEITED = "FORFEITED"
    FAILED = "FAILED"


class EscrowTransactionTypeEnum(str, Enum):
    HOLD = "HOLD"
    RELEASE = "RELEASE"
    REFUND = "REFUND"
    DEDUCTION = "DEDUCTION"
    ADJUSTMENT = "ADJUSTMENT"


class EscrowTransactionStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class EscrowRefundStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


class EscrowPartyTypeEnum(str, Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    CAR_OWNER = "CAR_OWNER"
    DRIVER = "DRIVER"
    VEHICLE_OWNER = "VEHICLE_OWNER"


class EscrowActionSourceEnum(str, Enum):
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"
    USER = "USER"
    PAYMENT_GATEWAY = "PAYMENT_GATEWAY"


class ClaimResolutionTypeEnum(str, Enum):
    FULL_DEDUCTION = "FULL_DEDUCTION"
    PARTIAL_DEDUCTION = "PARTIAL_DEDUCTION"
    FULL_REFUND = "FULL_REFUND"
    MANUAL_SETTLEMENT = "MANUAL_SETTLEMENT"


class DamageClaimStatusEnum(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    PARTIALLY_APPROVED = "PARTIALLY_APPROVED"
    REJECTED = "REJECTED"
    RESOLVED = "RESOLVED"


class DamageSeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ClaimEvidenceTypeEnum(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    PDF = "PDF"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"


class BookingReferenceTypeEnum(str, Enum):
    RIDE = "RIDE"
    RENTAL = "RENTAL"
    PARCEL = "PARCEL"


class LoyaltyTier(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class LoyaltyTransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    EXPIRED = "EXPIRED"
    ADJUSTMENT = "ADJUSTMENT"


class LoyaltyTransactionSource(str, Enum):
    RIDE = "RIDE"
    PARCEL = "PARCEL"
    REFERRAL = "REFERRAL"
    PROMOTION = "PROMOTION"
    ADMIN = "ADMIN"
    BONUS = "BONUS"
    WALLET_RECHARGE = "WALLET_RECHARGE"


class AddressType(str, Enum):
    HOME = "HOME"
    WORK = "WORK"
    OFFICE = "OFFICE"
    OTHER = "OTHER"


class PreferredLanguage(str, Enum):
    ENGLISH = "ENGLISH"
    TELUGU = "TELUGU"
    HINDI = "HINDI"
    TAMIL = "TAMIL"
    KANNADA = "KANNADA"
    MALAYALAM = "MALAYALAM"


class EmergencyContactRelation(str, Enum):
    FATHER = "FATHER"
    MOTHER = "MOTHER"
    BROTHER = "BROTHER"
    SISTER = "SISTER"
    SPOUSE = "SPOUSE"
    FRIEND = "FRIEND"
    RELATIVE = "RELATIVE"
    GUARDIAN = "GUARDIAN"
    OTHER = "OTHER"


class VehicleType(str, Enum):
    BIKE = "BIKE"
    SCOOTER = "SCOOTER"
    AUTO = "AUTO"
    HATCHBACK = "HATCHBACK"
    SEDAN = "SEDAN"
    SUV = "SUV"
    LUXURY = "LUXURY"
    ELECTRIC = "ELECTRIC"
    VAN = "VAN"
    TRUCK = "TRUCK"


class FuelType(str, Enum):
    PETROL = "PETROL"
    DIESEL = "DIESEL"
    ELECTRIC = "ELECTRIC"
    CNG = "CNG"
    HYBRID = "HYBRID"


class TransmissionType(str, Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"
    SEMI_AUTOMATIC = "SEMI_AUTOMATIC"


class VehicleVerificationStatus(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"


class CouponType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class CampaignStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class DriverDocumentType(str, Enum):
    DRIVING_LICENSE = "driving_license"
    AADHAR_CARD = "aadhar_card"
    PAN_CARD = "pan_card"
    VEHICLE_RC = "vehicle_rc"
    VEHICLE_INSURANCE = "vehicle_insurance"
    POLLUTION_CERTIFICATE = "pollution_certificate"
    PROFILE_PHOTO = "profile_photo"


class DriverStatus(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"
    PENDING_APPROVAL = "pending_approval"


class OnlineStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ON_RIDE = "on_ride"
    IDLE = "idle"


class PayoutMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    CASH = "cash"
    WALLET = "wallet"


class PayoutStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PenaltyStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    WAIVED = "waived"
    OVERDUE = "overdue"
    ACTIVE = "active"


class ShiftStatus(str, Enum):
    STARTED = "started"
    ENDED = "ended"
    BREAK = "break"
    MISSED = "missed"


class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"


class SubscriptionPlan(str, Enum):
    BASIC = "basic"
    PRO = "pro"




# =========================================================
# PARCEL ENUMS
# =========================================================

class ParcelStatus(str, Enum):
    CREATED = "created"
    REQUESTED = "requested"
    DRIVER_ASSIGNED = "driver_assigned"
    ACCEPTED = "accepted"
    PICKUP_STARTED = "pickup_started"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ParcelType(str, Enum):
    PACKAGE = "package"
    DOCUMENT = "document"
    SMALL = "small"
    LARGE = "large"
    FOOD = "food"


class ParcelPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class ParcelWeightTier(str, Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class ParcelPaymentType(str, Enum):
    PREPAID = "prepaid"
    COD = "cod"


class ProofType(str, Enum):
    PICKUP_PHOTO = "pickup_photo"
    DELIVERY_PHOTO = "delivery_photo"
    OTP = "otp"
    SIGNATURE = "signature"


class DeliveryAttemptStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"
    CANCELLED = "cancelled"


class ParcelCancellationReason(str, Enum):
    CUSTOMER_CANCELLED = "customer_cancelled"
    DRIVER_CANCELLED = "driver_cancelled"
    NO_DRIVER_FOUND = "no_driver_found"
    WRONG_ADDRESS = "wrong_address"
    PACKAGE_NOT_READY = "package_not_ready"
    RECEIVER_UNAVAILABLE = "receiver_unavailable"
    OTHER = "other"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class FeedbackType(str, Enum):
    DRIVER = "driver"
    CUSTOMER = "customer"
    DELIVERY = "delivery"
    PAYMENT = "payment"
    APP = "app"
    OTHER = "other"

class DiscountType(str, Enum):
    FLAT = "flat"
    PERCENTAGE = "percentage"

class InspectionType(str, Enum):
    PRE = "pre"
    POST = "post"
from enum import Enum


# =========================================================
# RIDE ENUMS
# =========================================================

class RideStatus(str, Enum):
    REQUESTED = "requested"
    DRIVER_ASSIGNED = "driver_assigned"
    ACCEPTED = "accepted"
    ARRIVED = "arrived"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class RideType(str, Enum):
    BIKE = "bike"
    AUTO = "auto"
    MINI = "mini"
    SEDAN = "sedan"
    SUV = "suv"
    LUXURY = "luxury"
    RENTAL = "rental"
    OUTSTATION = "outstation"


# =========================================================
# COMMON (REUSED)
# =========================================================

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class FeedbackType(str, Enum):
    DRIVER = "driver"
    CUSTOMER = "customer"
    RIDE = "ride"
    PAYMENT = "payment"
    APP = "app"
    OTHER = "other"


class DiscountType(str, Enum):
    FLAT = "flat"
    PERCENTAGE = "percentage"


# =========================================================
# EMERGENCY ENUMS
# =========================================================

class EmergencyAlertType(str, Enum):
    SOS = "sos"
    ACCIDENT = "accident"
    HARASSMENT = "harassment"
    MEDICAL = "medical"
    VEHICLE_ISSUE = "vehicle_issue"
    OTHER = "other"


class EmergencyAlertStatus(str, Enum):
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

    from enum import Enum


class ServiceType(str, Enum):
    BIKE = "bike"
    AUTO = "auto"
    MINI = "mini"
    SEDAN = "sedan"
    SUV = "suv"
    PARCEL = "parcel"
    RENTAL = "rental"


class TripStatus(str, Enum):
    SEARCHING = "searching"
    DRIVER_ASSIGNED = "driver_assigned"
    ACCEPTED = "accepted"
    ARRIVED = "arrived"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"