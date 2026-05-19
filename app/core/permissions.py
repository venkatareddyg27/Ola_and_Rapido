from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.core.dependencies import get_current_user


async def super_admin_required(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in ("SUPER_ADMIN", "SUPERADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only SuperAdmin can perform this action",
        )

    return current_user