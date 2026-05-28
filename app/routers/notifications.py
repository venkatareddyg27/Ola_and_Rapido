from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy import (
    select,
    update,
    delete,
    desc
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import get_db

from app.models.support import (
    Notification
)

from app.models.user_models import (
    User
)

from app.schemas.support import (
    NotificationCreate,
    NotificationResponse,
    NotificationMarkReadRequest
)

from app.core.security import (
    get_current_user
)

from app.core.websocket_manager import (
    websocket_manager
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"])


# =========================================================
# GET USER NOTIFICATIONS
# =========================================================

@router.get(
    "/",
    response_model=list[NotificationResponse]
)
async def get_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    unread_only: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * limit

    query = select(Notification).where(
        Notification.user_id == current_user.id
    )

    if unread_only:
        query = query.where(Notification.read_at == None)

    query = (
        query.order_by(desc(Notification.created_at))
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)

    notifications = (
        result.scalars().all()
    )

    return notifications


# =========================================================
# SEND NOTIFICATION
# =========================================================

@router.post(
    "/send",
    response_model=NotificationResponse
)
async def send_notification(
    payload: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send notification
    to specific user.
    """

    # =====================================================
    # CREATE NOTIFICATION
    # =====================================================

    notification = Notification(
        user_id=payload.user_id,
        title=payload.title,

        message=payload.message,

        notification_type=(
            payload.notification_type
        ),

        is_read=False
    )

    db.add(notification)

    await db.commit()

    await db.refresh(notification)

    # =====================================================
    # REALTIME WEBSOCKET EVENT
    # =====================================================

    await websocket_manager.send_to_user(
        user_id=str(payload.user_id),
        message={
            "event": "NEW_NOTIFICATION",

            "title": payload.title,

            "message": payload.message,

            "notification_id": (
                str(notification.id)
            )
        }
    )

    return notification


# =========================================================
# MARK NOTIFICATIONS AS READ
# =========================================================

@router.put("/mark-read")
async def mark_notification_read(
    payload: NotificationMarkReadRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await db.execute(
        update(Notification)
        .where(
            Notification.id == payload.notification_id,
            Notification.user_id == current_user.id
        )
        .values(read_at=datetime.utcnow())
    )

    await db.commit()

    return {
        "message": "Notification marked as read"
    }


@router.delete("/clear")
async def clear_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await db.execute(
        delete(Notification).where(
            Notification.user_id == current_user.id
        )
    )

    await db.commit()

    return {
        "message": "All notifications cleared"
    }