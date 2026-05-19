from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    OWNER = "OWNER"
    ADMIN = "ADMIN"


class UserStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class DriverStatus(str, Enum):
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    BUSY = "BUSY"
    ON_TRIP = "ON_TRIP"


class SubscriptionPlan(str, Enum):
    BASIC = "BASIC"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class OTPPurpose(str, Enum):
    LOGIN = "LOGIN"
    REGISTER = "REGISTER"
    RESET_PASSWORD = "RESET_PASSWORD"
    VERIFY_PHONE = "VERIFY_PHONE"