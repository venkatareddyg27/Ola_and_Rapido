from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.support import Notification
from app.models.user_models import User
from app.core.websocket_manager import websocket_manager
from app.core.firebase import send_push_notification


async def notify_user(
    db: AsyncSession,
    user_id,
    title: str,
    body: str,
    notification_type: str,
    data: dict | None = None
):
    notification = Notification(
        user_id=user_id,
        title=title,
        body=body,
        type=notification_type,
        data=data or {},
        read_at=None
    )

    db.add(notification)
    await db.commit()
    await db.refresh(notification)

    websocket_payload = {
        "event": "NEW_NOTIFICATION",
        "notification_id": str(notification.id),
        "title": title,
        "body": body,
        "type": notification_type,
        "data": data or {}
    }

    await websocket_manager.send_to_user(
        user_id=str(user_id),
        message=websocket_payload
    )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user and user.fcm_token:
        await send_push_notification(
            token=user.fcm_token,
            title=title,
            body=body,
            data={
                "notification_id": str(notification.id),
                "type": notification_type,
                **(data or {})
            }
        )

    return notification