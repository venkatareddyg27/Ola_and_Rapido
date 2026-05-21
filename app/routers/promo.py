# promo.py

from uuid import UUID
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import (
    select,
    and_
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.user_models import User
from app.models.operations import PromoCode

from app.schemas.operations import (
    PromoApplyRequest,
    PromoApplyResponse,
    PromoCreate,
    PromoResponse
)

from app.core.security import (
    get_current_user
)

from app.core.enums import (
    UserRole
)

router = APIRouter(
    prefix="/promo",
    tags=["Promotions"]
)


# =========================================================
# APPLY PROMO CODE
# =========================================================

@router.post(
    "/apply",
    response_model=PromoApplyResponse
)
async def apply_promo(
    payload: PromoApplyRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Apply promo code and calculate discount.
    """

    # =====================================================
    # GET PROMO
    # =====================================================

    result = await db.execute(
        select(PromoCode).where(
            PromoCode.code == payload.code,
            PromoCode.is_active == True
        )
    )

    promo = result.scalars().first()

    if not promo:

        raise HTTPException(
            status_code=404,
            detail="Invalid promo code"
        )

    # =====================================================
    # VALIDATE EXPIRY
    # =====================================================

    if promo.valid_till < datetime.utcnow():

        raise HTTPException(
            status_code=400,
            detail="Promo code expired"
        )

    # =====================================================
    # VALIDATE MINIMUM AMOUNT
    # =====================================================

    if payload.trip_amount < promo.min_trip_amount:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Minimum trip amount should be "
                f"{promo.min_trip_amount}"
            )
        )

    # =====================================================
    # CALCULATE DISCOUNT
    # =====================================================

    discount = (
        payload.trip_amount *
        promo.discount_percent
    ) / 100

    # =====================================================
    # MAX DISCOUNT LIMIT
    # =====================================================

    if promo.max_discount_amount:

        discount = min(
            discount,
            promo.max_discount_amount
        )

    final_amount = (
        payload.trip_amount - discount
    )

    return {
        "promo_code": promo.code,
        "discount_amount": round(discount, 2),
        "final_amount": round(final_amount, 2)
    }


# =========================================================
# GET ACTIVE PROMOS
# =========================================================

@router.get(
    "/active",
    response_model=list[PromoResponse]
)
async def get_active_promos(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all active promo codes.
    """

    result = await db.execute(
        select(PromoCode).where(
            PromoCode.is_active == True,
            PromoCode.valid_till > datetime.utcnow()
        )
    )

    promos = result.scalars().all()

    return promos


# =========================================================
# ADMIN CREATE PROMO
# =========================================================

@router.post(
    "/create",
    response_model=PromoResponse
)
async def create_promo(
    payload: PromoCreate,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):
    """
    Admin creates promo code.
    """

    # =====================================================
    # ADMIN VALIDATION
    # =====================================================

    if current_user.role != UserRole.ADMIN:

        raise HTTPException(
            status_code=403,
            detail="Only admin can create promos"
        )

    # =====================================================
    # CHECK EXISTING CODE
    # =====================================================

    result = await db.execute(
        select(PromoCode).where(
            PromoCode.code == payload.code
        )
    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Promo code already exists"
        )

    # =====================================================
    # CREATE PROMO
    # =====================================================

    promo = PromoCode(
        code=payload.code.upper(),

        description=payload.description,

        discount_percent=payload.discount_percent,

        max_discount_amount=payload.max_discount_amount,

        min_trip_amount=payload.min_trip_amount,

        valid_till=payload.valid_till,

        is_active=True,

        creator_id=current_user.id
    )

    db.add(promo)

    await db.commit()

    await db.refresh(promo)

    return promo