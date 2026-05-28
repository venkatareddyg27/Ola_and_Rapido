from uuid import UUID
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.enums import (PaymentMethod,PaymentStatus, WalletTransactionType,)
from app.models.payments import Payment, Wallet, WalletTransaction
from app.schemas.payments import (PaymentCreate,PaymentResponse,WalletResponse,)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-order", response_model=PaymentResponse)
async def create_payment_order(
    payload: PaymentCreate,
    db: AsyncSession = Depends(get_db),
):
    payment = Payment(
        user_id=payload.user_id,
        trip_id=payload.trip_id,
        rental_id=payload.rental_id,
        amount=payload.amount,
        method=payload.method,
        status=PaymentStatus.PENDING,
        gateway_reference=None,
    )

    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    return payment


@router.post("/verify", response_model=PaymentResponse)
async def verify_payment(
    payment_id: UUID,
    gateway_reference: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).where(Payment.id == payment_id)
    )
    payment = result.scalar_one_or_none()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.status = PaymentStatus.SUCCESS
    payment.gateway_reference = gateway_reference

    await db.commit()
    await db.refresh(payment)

    return payment


@router.get("/history", response_model=list[PaymentResponse])
async def get_payment_history(
    user_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * limit

    result = await db.execute(
        select(Payment)
        .where(Payment.user_id == user_id)
        .order_by(Payment.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return result.scalars().all()


@router.post("/wallet/topup", response_model=WalletResponse)
async def wallet_topup(
    user_id: UUID,
    amount: Decimal,
    gateway_reference: str,
    db: AsyncSession = Depends(get_db),
):
    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero",
        )

    result = await db.execute(
        select(Wallet).where(Wallet.user_id == user_id)
    )
    wallet = result.scalar_one_or_none()

    if not wallet:
        wallet = Wallet(
            user_id=user_id,
            balance=Decimal("0.00"),
            currency="INR",
        )
        db.add(wallet)
        await db.flush()

    wallet.balance = Decimal(str(wallet.balance)) + amount

    payment = Payment(
        user_id=user_id,
        amount=amount,
        method=PaymentMethod.WALLET,
        status=PaymentStatus.SUCCESS,
        gateway_reference=gateway_reference,
    )

    transaction = WalletTransaction(
        wallet_id=wallet.id,
        type=WalletTransactionType.CREDIT,
        amount=amount,
        reason="Wallet topup",
        reference_id=gateway_reference,
    )

    db.add(payment)
    db.add(transaction)

    await db.commit()
    await db.refresh(wallet)

    return wallet