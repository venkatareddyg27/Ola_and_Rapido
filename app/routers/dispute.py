from typing import List
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.enums import DisputeStatus
from app.models.support import Dispute
from app.schemas.support import (
    DisputeCreate,
    DisputeResponse,
    DisputeUpdate,
)

router = APIRouter(prefix="/disputes", tags=["Disputes"])


@router.post(
    "/",
    response_model=DisputeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_dispute(
    payload: DisputeCreate,
    db: AsyncSession = Depends(get_db),
):
    dispute = Dispute(
        user_id=payload.user_id,
        trip_id=payload.trip_id,
        rental_id=payload.rental_id,
        category=payload.category,
        description=payload.description,
        priority=payload.priority,
        status=DisputeStatus.OPEN,
    )

    db.add(dispute)
    await db.commit()
    await db.refresh(dispute)

    return dispute


@router.get("/", response_model=List[DisputeResponse])
async def get_user_disputes(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dispute).where(Dispute.user_id == user_id)
    )

    return result.scalars().all()


@router.put("/{dispute_id}/resolve", response_model=DisputeResponse)
async def resolve_dispute(
    dispute_id: UUID,
    payload: DisputeUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dispute).where(Dispute.id == dispute_id)
    )

    dispute = result.scalar_one_or_none()

    if not dispute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispute not found",
        )

    dispute.status = DisputeStatus.RESOLVED
    dispute.resolution = payload.resolution
    dispute.resolved_by = payload.resolved_by
    dispute.resolved_at = payload.resolved_at or datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(dispute)

    return dispute