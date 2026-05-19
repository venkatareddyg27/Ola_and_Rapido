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
    

class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


# =========================================================
# PAYMENT METHOD TYPE ENUM
# =========================================================

class PaymentMethodTypeEnum(str, Enum):
    CARD = "CARD"
    UPI = "UPI"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"
    CASH = "CASH"


# =========================================================
# WALLET TRANSACTION TYPE ENUM
# =========================================================

class WalletTransactionTypeEnum(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


# =========================================================
# RECHARGE STATUS ENUM
# =========================================================

class WalletRechargeStatusEnum(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# =========================================================
# PAYMENT TRANSACTION STATUS ENUM
# =========================================================

class PaymentTransactionStatusEnum(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"


# =========================================================
# REFUND STATUS ENUM
# =========================================================

class RefundStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


# =========================================================
# INVOICE STATUS ENUM
# =========================================================

class InvoiceStatusEnum(str, Enum):
    GENERATED = "GENERATED"
    SENT = "SENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


# =========================================================
# SETTLEMENT STATUS ENUM
# =========================================================

class SettlementStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# =========================================================
# GATEWAY NAME ENUM
# =========================================================

class PaymentGatewayEnum(str, Enum):
    RAZORPAY = "RAZORPAY"
    STRIPE = "STRIPE"
    PAYTM = "PAYTM"
    PHONEPE = "PHONEPE"
    CASHFREE = "CASHFREE"


# =========================================================
# CURRENCY ENUM
# =========================================================

class CurrencyEnum(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"


# =========================================================
# REFERENCE TYPE ENUM
# =========================================================

class PaymentReferenceTypeEnum(str, Enum):
    RIDE = "RIDE"
    PARCEL = "PARCEL"
    RENTAL = "RENTAL"
    WALLET_RECHARGE = "WALLET_RECHARGE"
    ESCROW = "ESCROW"


# =========================================================
# GATEWAY LOG STATUS ENUM
# =========================================================

class GatewayLogStatusEnum(str, Enum):
    REQUESTED = "REQUESTED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


# =========================================================
# TAX TYPE ENUM
# =========================================================

class TaxTypeEnum(str, Enum):
    CGST = "CGST"
    SGST = "SGST"
    IGST = "IGST"


# =========================================================
# PAYMENT SOURCE ENUM
# =========================================================

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


# =========================================================
# ESCROW TRANSACTION TYPE ENUM
# =========================================================

class EscrowTransactionTypeEnum(str, Enum):
    HOLD = "HOLD"
    RELEASE = "RELEASE"
    REFUND = "REFUND"
    DEDUCTION = "DEDUCTION"
    ADJUSTMENT = "ADJUSTMENT"


# =========================================================
# ESCROW TRANSACTION STATUS ENUM
# =========================================================

class EscrowTransactionStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# =========================================================
# DAMAGE CLAIM STATUS ENUM
# =========================================================

class DamageClaimStatusEnum(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    PARTIALLY_APPROVED = "PARTIALLY_APPROVED"
    REJECTED = "REJECTED"
    RESOLVED = "RESOLVED"


# =========================================================
# DAMAGE SEVERITY ENUM
# =========================================================

class DamageSeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# =========================================================
# CLAIM EVIDENCE TYPE ENUM
# =========================================================

class ClaimEvidenceTypeEnum(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    PDF = "PDF"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"


# =========================================================
# ESCROW REFUND STATUS ENUM
# =========================================================

class EscrowRefundStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


# =========================================================
# BOOKING REFERENCE TYPE ENUM
# =========================================================

class BookingReferenceTypeEnum(str, Enum):
    RIDE = "RIDE"
    RENTAL = "RENTAL"
    PARCEL = "PARCEL"


# =========================================================
# ESCROW PARTY TYPE ENUM
# =========================================================

class EscrowPartyTypeEnum(str, Enum):
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    VEHICLE_OWNER = "VEHICLE_OWNER"
    ADMIN = "ADMIN"


# =========================================================
# CLAIM RESOLUTION TYPE ENUM
# =========================================================

class ClaimResolutionTypeEnum(str, Enum):
    FULL_DEDUCTION = "FULL_DEDUCTION"
    PARTIAL_DEDUCTION = "PARTIAL_DEDUCTION"
    FULL_REFUND = "FULL_REFUND"
    MANUAL_SETTLEMENT = "MANUAL_SETTLEMENT"


# =========================================================
# ESCROW ACTION SOURCE ENUM
# =========================================================

class EscrowActionSourceEnum(str, Enum):
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"
    USER = "USER"
    PAYMENT_GATEWAY = "PAYMENT_GATEWAY"
    
class LoyaltyTier(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"

class AddressType(str, Enum):
    HOME = "HOME"
    WORK = "WORK"
    OFFICE = "OFFICE"
    OTHER = "OTHER"


# =========================================================
# PREFERRED LANGUAGE ENUM
# =========================================================

class PreferredLanguage(str, Enum):
    ENGLISH = "ENGLISH"
    TELUGU = "TELUGU"
    HINDI = "HINDI"
    TAMIL = "TAMIL"
    KANNADA = "KANNADA"
    MALAYALAM = "MALAYALAM"


# =========================================================
# EMERGENCY CONTACT RELATION ENUM
# =========================================================

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
# LOYALTY TRANSACTION TYPE ENUM
# =========================================================

class LoyaltyTransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    EXPIRED = "EXPIRED"
    ADJUSTMENT = "ADJUSTMENT"


# =========================================================
# LOYALTY TRANSACTION SOURCE ENUM
# =========================================================

class LoyaltyTransactionSource(str, Enum):
    RIDE = "RIDE"
    PARCEL = "PARCEL"
    REFERRAL = "REFERRAL"
    PROMOTION = "PROMOTION"
    ADMIN = "ADMIN"
    BONUS = "BONUS"
    WALLET_RECHARGE = "WALLET_RECHARGE"


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


# =========================================================
# FUEL TYPE ENUM
# =========================================================

class FuelType(str, Enum):
    PETROL = "PETROL"
    DIESEL = "DIESEL"
    ELECTRIC = "ELECTRIC"
    CNG = "CNG"
    HYBRID = "HYBRID"


# =========================================================
# TRANSMISSION TYPE ENUM
# =========================================================

class TransmissionType(str, Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"
    SEMI_AUTOMATIC = "SEMI_AUTOMATIC"


# =========================================================
# VEHICLE VERIFICATION STATUS ENUM
# =========================================================

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


# =========================================================
# ATTENDANCE STATUS
# =========================================================

class AttendanceStatus(str,Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


# =========================================================
# DRIVER DOCUMENT TYPE
# =========================================================

class DriverDocumentType(str,Enum):
    DRIVING_LICENSE = "driving_license"
    AADHAR_CARD = "aadhar_card"
    PAN_CARD = "pan_card"
    VEHICLE_RC = "vehicle_rc"
    VEHICLE_INSURANCE = "vehicle_insurance"
    POLLUTION_CERTIFICATE = "pollution_certificate"
    PROFILE_PHOTO = "profile_photo"


# =========================================================
# DRIVER STATUS
# =========================================================

class DriverStatus(str,Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    SUSPENDED = "suspended"
    PENDING_APPROVAL = "pending_approval"


# =========================================================
# ONLINE STATUS
# =========================================================

class OnlineStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ON_RIDE = "on_ride"
    IDLE = "idle"


# =========================================================
# PAYOUT METHOD
# =========================================================

class PayoutMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    CASH = "cash"
    WALLET = "wallet"


# =========================================================
# PAYOUT STATUS
# =========================================================

class PayoutStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# =========================================================
# PENALTY STATUS
# =========================================================

class PenaltyStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    WAIVED = "waived"
    OVERDUE = "overdue"
    ACTIVE = "active"


# =========================================================
# SHIFT STATUS
# =========================================================

class ShiftStatus(str, Enum):
    STARTED = "started"
    ENDED = "ended"
    BREAK = "break"
    MISSED = "missed"


# =========================================================
# VERIFICATION STATUS
# =========================================================
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    WAIVED = "WAIVED"

# =========================================================
# RENTAL BOOKING
# =========================================================
 
class RentalBookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
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
    PENDING = "PENDING"
 
class RentalExtensionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
 
 
class ChecklistType(str, Enum):
    PICKUP = "pickup"
    RETURN = "return"
  
# =========================================================
# PAYMENT ENUMS
# =========================================================
 
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
 
 
# =========================================================
# ESCROW ENUMS
# =========================================================
 
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
 
 
# =========================================================
# PARCEL ENUMS
# =========================================================
 
class PackageType(str, Enum):
    DOCUMENT = "document"
    FOOD = "food"
    ELECTRONICS = "electronics"
    GROCERY = "grocery"
    MEDICINE = "medicine"
    CLOTHES = "clothes"
    OTHERS = "others"
 
 
class WeightTier(str, Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
 
 
class ParcelStatus(str, Enum):
    PENDING_PICKUP = "pending_pickup"
    DRIVER_ASSIGNED = "driver_assigned"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED_DELIVERY = "failed_delivery"
    RETURNED = "returned"
    CANCELLED = "cancelled"
 
 
class ParcelTrackingStatus(str, Enum):
    DRIVER_ASSIGNED = "driver_assigned"
    PICKED_UP = "picked_up"
    REACHED_HUB = "reached_hub"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
 
 
class DeliveryAttemptStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RESCHEDULED = "rescheduled"
 
 
class ProofType(str, Enum):
    IMAGE = "image"
    SIGNATURE = "signature"
    OTP = "otp"
 
 
class FeedbackRating(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
 
 
# =========================================================
# USER ENUMS
# =========================================================
 
class UserTypeEnum(str, Enum):
    DRIVER = "driver"
    CUSTOMER = "customer"
 
 
class ActionTypeEnum(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    BAN = "ban"
    UNBAN = "unban"
    REFUND = "refund"
    ESCALATE = "escalate"
    RESOLVE = "resolve"
    ASSIGN = "assign"
    EXPORT = "export"
 
 
class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    DRIVER = "DRIVER"
    STORE_MANAGER = "STORE_MANAGER"
 
 
class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
 
 
# =========================================================
# KYC ENUMS
# =========================================================
 
class KYCStatus(str, Enum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
 
 class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"
 
 
class DocumentType(str, Enum):
    AADHAAR = "aadhaar"
    PAN = "pan"
    DRIVING_LICENSE = "driving_license"
    RC = "rc"
    INSURANCE = "insurance"
    PUC = "puc"
    SELFIE = "selfie"
 
 
class AadhaarEkycStatus(str, Enum):
    OTP_SENT = "otp_sent"
    OTP_VERIFIED = "otp_verified"
    COMPLETED = "completed"
    FAILED = "failed"
 
 
# =========================================================
# LOYALTY ENUMS
# =========================================================
 
class LoyaltyTier(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
 
 
# =========================================================
# DRIVER ENUMS
# =========================================================
 
class DriverStatus(str, Enum):
    IDLE = "idle"
    ON_RIDE = "on_ride"
    ON_DELIVERY = "on_delivery"
    PENDING = "PENDING"
    OFFLINE = "offline"
    BREAK = "break"
 
 
# =========================================================
# VEHICLE ENUMS
# =========================================================
 
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
# RIDE ENUMS
# =========================================================
 
class RideType(str, Enum):
    CITY = "city"
    OUTSTATION = "outstation"
    RENTAL = "rental"
 
 
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
 
 
# =========================================================
# RENTAL ENUMS
# =========================================================
 
class RentalBookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
 
 

