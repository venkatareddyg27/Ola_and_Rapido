from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.user_models import User

from app.core.enums import (
    UserRole,
    UserStatus
)

# =========================================================
# CREATE DEFAULT ADMIN
# =========================================================

async def create_default_admin(
    db: AsyncSession
):

    admin_mobile = "+919999999999"

    # CHECK EXISTING ADMIN

    result = await db.execute(

        select(User).where(
            User.mobile_number ==
            admin_mobile
        )
    )

    existing_admin = (
        result.scalar_one_or_none()
    )

    if existing_admin:

        return

    # CREATE ADMIN

    admin = User(

        mobile_number=
        admin_mobile,

        first_name=
        "Super",

        last_name=
        "Admin",

        full_name=
        "Super Admin",

        role=
        UserRole.ADMIN,

        status=
        UserStatus.ACTIVE
    )

    db.add(admin)

    await db.commit()

    print(
        "Default admin created successfully"
    )