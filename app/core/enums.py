
from enum import Enum


# =========================================================
# ENUMS
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