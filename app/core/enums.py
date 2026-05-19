from enum import Enum


# =========================================================
# USER ROLE ENUM
# =========================================================

class UserRoleEnum(str, Enum):
    USER = "USER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    STORE_MANAGER = "STORE_MANAGER"


# =========================================================
# GENDER ENUM
# =========================================================

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


# =========================================================
# DEVICE TYPE ENUM
# =========================================================

class DeviceTypeEnum(str, Enum):
    ANDROID = "ANDROID"
    IOS = "IOS"
    WEB = "WEB"


# =========================================================
# OTP PURPOSE ENUM
# =========================================================

class OTPPurposeEnum(str, Enum):
    LOGIN = "LOGIN"
    REGISTER = "REGISTER"
    PASSWORD_RESET = "PASSWORD_RESET"
    MOBILE_VERIFICATION = "MOBILE_VERIFICATION"


# =========================================================
# LOGIN STATUS ENUM
# =========================================================

class LoginStatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


# =========================================================
# BLOCK STATUS ENUM
# =========================================================

class BlockStatusEnum(str, Enum):
    TEMPORARY = "TEMPORARY"
    PERMANENT = "PERMANENT"


# =========================================================
# PERMISSION ENUM
# =========================================================

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


# =========================================================
# ROLE NAME ENUM
# =========================================================

class RoleNameEnum(str, Enum):
    USER = "USER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    FINANCE_MANAGER = "FINANCE_MANAGER"


# =========================================================
# ACCOUNT STATUS ENUM
# =========================================================

class AccountStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"
    SUSPENDED = "SUSPENDED"


# =========================================================
# TOKEN TYPE ENUM
# =========================================================

class TokenTypeEnum(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
    RESET = "RESET"


# =========================================================
# PASSWORD RESET STATUS ENUM
# =========================================================

class PasswordResetStatusEnum(str, Enum):
    PENDING = "PENDING"
    USED = "USED"
    EXPIRED = "EXPIRED"


# =========================================================
# PAYMENT ENUMS
# =========================================================

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


# =========================================================
# ESCROW ENUMS
# =========================================================

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


class BookingReferenceTypeEnum(str, Enum):
    RIDE = "RIDE"
    RENTAL = "RENTAL"
    PARCEL = "PARCEL"


class EscrowPartyTypeEnum(str, Enum):
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    VEHICLE_OWNER = "VEHICLE_OWNER"
    ADMIN = "ADMIN"


class ClaimResolutionTypeEnum(str, Enum):
    FULL_DEDUCTION = "FULL_DEDUCTION"
    PARTIAL_DEDUCTION = "PARTIAL_DEDUCTION"
    FULL_REFUND = "FULL_REFUND"
    MANUAL_SETTLEMENT = "MANUAL_SETTLEMENT"


class EscrowActionSourceEnum(str, Enum):
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"
    USER = "USER"
    PAYMENT_GATEWAY = "PAYMENT_GATEWAY"


# =========================================================
# DAMAGE CLAIM ENUMS
# =========================================================

class DamageClaimStatus(str, Enum):
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


# =========================================================
# LOYALTY ENUMS
# =========================================================

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


# =========================================================
# ADDRESS / LANGUAGE / CONTACT
# =========================================================

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


# =========================================================
# VEHICLE ENUMS
# =========================================================

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


# =========================================================
# DRIVER ENUMS
# =========================================================

class DriverStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    BLOCKED = "BLOCKED"


class OnlineStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    ON_TRIP = "ON_TRIP"


class DriverDocumentType(str, Enum):
    LICENSE = "LICENSE"
    AADHAAR = "AADHAAR"
    PAN = "PAN"
    RC = "RC"
    INSURANCE = "INSURANCE"
    PUC = "PUC"
    SELFIE = "SELFIE"


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class PayoutStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class PayoutMethod(str, Enum):
    BANK = "BANK"
    UPI = "UPI"
    WALLET = "WALLET"


class ShiftStatus(str, Enum):
    STARTED = "STARTED"
    ENDED = "ENDED"
    BREAK = "BREAK"


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    HALF_DAY = "HALF_DAY"


class PenaltyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    WAIVED = "WAIVED"


# =========================================================
# RENTAL ENUMS
# =========================================================

class RentalBookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class RentalExtensionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ChecklistType(str, Enum):
    PICKUP = "PICKUP"
    RETURN = "RETURN"


# =========================================================
# PARCEL ENUMS
# =========================================================

class PackageType(str, Enum):
    DOCUMENT = "DOCUMENT"
    FOOD = "FOOD"
    ELECTRONICS = "ELECTRONICS"
    GROCERY = "GROCERY"
    MEDICINE = "MEDICINE"
    CLOTHES = "CLOTHES"
    OTHERS = "OTHERS"


class WeightTier(str, Enum):
    LIGHT = "LIGHT"
    MEDIUM = "MEDIUM"
    HEAVY = "HEAVY"


class ParcelStatus(str, Enum):
    PENDING_PICKUP = "PENDING_PICKUP"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    FAILED_DELIVERY = "FAILED_DELIVERY"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


class ParcelTrackingStatus(str, Enum):
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    PICKED_UP = "PICKED_UP"
    REACHED_HUB = "REACHED_HUB"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"


class DeliveryAttemptStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RESCHEDULED = "RESCHEDULED"


class ProofType(str, Enum):
    IMAGE = "IMAGE"
    SIGNATURE = "SIGNATURE"
    OTP = "OTP"


class FeedbackRating(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


# =========================================================
# RIDE ENUMS
# =========================================================

class RideType(str, Enum):
    CITY = "CITY"
    OUTSTATION = "OUTSTATION"
    RENTAL = "RENTAL"


class RideStatus(str, Enum):
    SEARCHING = "SEARCHING"
    ACCEPTED = "ACCEPTED"
    ARRIVED = "ARRIVED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    UPI = "UPI"
    CARD = "CARD"
    WALLET = "WALLET"