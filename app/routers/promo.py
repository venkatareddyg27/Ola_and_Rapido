from uuid import UUID
from datetime import datetime
from fastapi import (APIRouter,Depends,HTTPException)
from sqlalchemy import (select)
from sqlalchemy.ext.asyncio import (AsyncSession)
from app.core.database import (get_db)
from app.models.user_models import (User)
from app.models.operations import (PromoCode)
from app.schemas.operations import (PromoApplyRequest,PromoApplyResponse,PromoCreate, PromoResponse)
from app.core.security import (get_current_user)
from app.core.enums import (UserRole,DiscountType)

router = APIRouter(prefix="/promo",tags=["Promotions"])


@router.post("/apply",response_model=PromoApplyResponse)
async def apply_promo(

    payload: PromoApplyRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )):

    result = await db.execute(

        select(PromoCode)

        .where(
            PromoCode.code ==
            payload.code.upper()
        )

        .where(
            PromoCode.active == True
        )

    )

    promo = result.scalars().first()

    if not promo:

        raise HTTPException(

            status_code=404,

            detail="Invalid promo code"

        )

    current_time = datetime.utcnow()

    if (
        promo.valid_from
        and
        promo.valid_from > current_time
    ):

        raise HTTPException(

            status_code=400,

            detail="Promo code not started yet"

        )

    if (
        promo.valid_until
        and
        promo.valid_until < current_time
    ):

        raise HTTPException(

            status_code=400,

            detail="Promo code expired"

        )

    if (
        promo.min_order
        and
        payload.order_amount
        < promo.min_order
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                f"Minimum order amount "
                f"should be "
                f"{promo.min_order}"
            )

        )

    if (
        promo.usage_limit
        and
        promo.used_count
        >=
        promo.usage_limit
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "Promo usage limit exceeded"
            )

        )

    if (
        promo.service_types
        and
        payload.service_type
        not in promo.service_types
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "Promo not applicable "
                "for this service"
            )

        )

    discount = 0

    if (
        promo.discount_type
        ==
        DiscountType.PERCENTAGE
    ):

        discount = (

            payload.order_amount

            * promo.discount_value

        ) / 100

    else:

        discount = (
            promo.discount_value
        )

    if promo.max_discount:

        discount = min(

            discount,

            promo.max_discount

        )

    final_amount = (

        payload.order_amount
        - discount

    )

    if final_amount < 0:

        final_amount = 0

    promo.used_count += 1

    await db.commit()

    return {

        "promo_code":
        promo.code,

        "discount_amount":
        round(discount, 2),

        "final_amount":
        round(final_amount, 2)

    }


@router.get(
    "/active",
    response_model=list[PromoResponse]
)
async def get_active_promos(

    db: AsyncSession = Depends(
        get_db
    )

):

    current_time = datetime.utcnow()

    result = await db.execute(

        select(PromoCode)

        .where(
            PromoCode.active == True
        )

    )

    promos = result.scalars().all()

    active_promos = []

    for promo in promos:

        if (
            promo.valid_from
            and
            promo.valid_from > current_time
        ):

            continue

        if (

            promo.valid_until

            and

            promo.valid_until
            < current_time

        ):

            continue

        if (
            promo.usage_limit
            and
            promo.used_count >= promo.usage_limit
        ):

            continue

        active_promos.append(
            promo
        )

    return active_promos


@router.post(
    "/create",
    response_model=PromoResponse
)
async def create_promo(

    payload: PromoCreate,

    db: AsyncSession = Depends(
        get_db
    ),

    current_user: User = Depends(
        get_current_user
    )

):

    if current_user.role != UserRole.ADMIN:

        raise HTTPException(

            status_code=403,

            detail=(
                "Only admin "
                "can create promos"
            )

        )

    result = await db.execute(

        select(PromoCode)

        .where(
            PromoCode.code
            ==
            payload.code.upper()
        )

    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(

            status_code=400,

            detail=(
                "Promo code "
                "already exists"
            )

        )


    if payload.discount_value <= 0:

        raise HTTPException(

            status_code=400,

            detail=(
                "Discount value "
                "must be greater than 0"
            )

        )

    valid_from = (
        payload.valid_from
        if payload.valid_from
        else None
    )

    valid_until = (
        payload.valid_until
        if payload.valid_until
        else None
    )

    if (
        valid_until
        and
        valid_from
        and
        valid_until < valid_from
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "valid_until must be "
                "greater than valid_from"
            )

        )

    promo = PromoCode(

        code=payload.code.upper(),

        description=payload.description,

        discount_type=
        payload.discount_type,

        discount_value=
        payload.discount_value,

        max_discount=
        payload.max_discount,

        min_order=
        payload.min_order,

        usage_limit=
        payload.usage_limit,

        used_count=0,

        valid_from=
        valid_from,

        valid_until=
        valid_until,

        service_types=
        payload.service_types,

        active=True,

        created_by=
        current_user.id

    )

    db.add(promo)

    await db.commit()

    await db.refresh(promo)

    return promo