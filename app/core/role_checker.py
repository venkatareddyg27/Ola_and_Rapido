from fastapi import HTTPException
from app.core.enums import UserRole


def require_customer_role(current_user):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403,detail="Only customers can access this API")


def require_driver_role(current_user):
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(status_code=403,detail="Only drivers can access this API")


def require_admin_role(current_user):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403,detail="Only admins can access this API")