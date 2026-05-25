from uuid import UUID
from decimal import Decimal
from datetime import datetime, timedelta
from fastapi import ( APIRouter, Depends, HTTPException, Query, status )
from sqlalchemy import ( select, func )
from sqlalchemy.ext.asyncio import ( AsyncSession )
from app.core.database import ( get_db )
from app.core.security import ( get_current_user )
from app.models.user_models import ( User )
from app.models.trips import ( Trip )
from app.models.support import ( Dispute )
from app.models.payments import ( Payment )
from app.models.operations import ( SurgeZone, AuditLog )
from app.schemas.admin import ( UserSuspendRequest, DisputeResolveRequest, SurgeOverrideRequest, BroadcastNotificationRequest )
from app.core.enums import ( UserRole, UserStatus )

router = APIRouter( prefix="/admin", tags=["Admin"] )

def require_admin( current_user: User):

    if current_user.role != UserRole.ADMIN:

        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = "Admin access required" )

@router.get("/live-ops")
async def get_live_operations( db: AsyncSession = Depends(get_db),current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    active_drivers = await db.scalar( select(func.count()).select_from(User).where( User.role == UserRole.DRIVER ))

    live_trips = await db.scalar( select(func.count()).select_from(Trip).where( Trip.status == "ONGOING" ) )

    return { "success": True, "data": { "active_drivers": active_drivers,
"live_trips": live_trips, "demand_supply_ratio": 1.4, "zones": [ { "zone": "Hyderabad Central", "active_rides": 120, "surge_multiplier": 1.8 },{ "zone": "Madhapur", "active_rides": 85, "surge_multiplier": 1.5 } ] } }

@router.get("/users")
async def get_users( page: int = Query(1, ge=1), limit: int = Query(10, le=100), role: str | None = None, search: str | None = None, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    query = select(User)

    if role:

        query = query.where( User.role == role )

    if search:

        query = query.where( User.full_name.ilike( f"%{search}%" ) )

    offset = (page - 1) * limit

    query = (query.offset(offset).limit(limit) )

    result = await db.execute(query)

    users = result.scalars().all()

    return { "success": True, "page": page, "limit": limit, "count": len(users), "items": users }

@router.put("/users/{user_id}/suspend")
async def suspend_user( user_id: UUID, payload: UserSuspendRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(User).where( User.id == user_id ) )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException( status_code=404, detail="User not found" )

    user.status = ( UserStatus.SUSPENDED if payload.suspend else UserStatus.ACTIVE )

    await db.commit()

    return { "success": True, "message": ( "User suspended successfully" if payload.suspend else "User reinstated successfully" ) }


@router.get("/disputes")
async def get_disputes( status_filter: str | None = None, page: int = Query(1, ge=1), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    query = select(Dispute)

    if status_filter: query = query.where( Dispute.status == status_filter )

    offset = (page - 1) * limit

    query = ( query.offset(offset).limit(limit) )

    result = await db.execute(query)

    disputes = result.scalars().all()

    return { "success": True, "count": len(disputes), "items": disputes }

@router.put("/disputes/{dispute_id}/resolve")
async def resolve_dispute(

    dispute_id: UUID,

    payload: DisputeResolveRequest,

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(Dispute).where( Dispute.id == dispute_id ) )

    dispute = result.scalar_one_or_none()

    if not dispute:

        raise HTTPException( status_code=404, detail="Dispute not found" )

    dispute.status = "RESOLVED"

    dispute.resolution_type = ( payload.resolution_type )

    dispute.refund_amount = ( payload.refund_amount )

    await db.commit()

    return { "success": True, "message": "Dispute resolved successfully" }

@router.get("/finance")
async def get_finance_summary( db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    total_revenue = await db.scalar( select( func.sum( Payment.amount ) ) )

    return { "success": True, "data": { "total_revenue": total_revenue or 0, "commissions": 120000, "payouts": 90000, "refunds": 15000 } }

@router.post("/surge/override")
async def override_surge( payload: SurgeOverrideRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    result = await db.execute( select(SurgeZone).where( SurgeZone.id == payload.zone_id ) )

    zone = result.scalar_one_or_none()

    if not zone:
        raise HTTPException( status_code=404, detail= "Surge zone not found" )

    zone.multiplier = ( payload.multiplier )

    await db.commit()

    return { "success": True, "message": "Surge pricing updated successfully" }

@router.post("/notifications/broadcast")
async def broadcast_notification( payload: BroadcastNotificationRequest, current_user: User = Depends( get_current_user )):

    require_admin(current_user)

    return { "success": True, "message": "Broadcast notification queued","target_segment": payload.target_segment }

@router.get("/analytics")
async def get_platform_analytics( db: AsyncSession = Depends(get_db), current_user: User = Depends( get_current_user ) ):

    require_admin(current_user)

    total_users = await db.scalar( select(func.count()).select_from(User) )

    total_trips = await db.scalar( select(func.count()) .select_from(Trip) )

    return {"success": True, "data": { "total_users": total_users, "total_trips": total_trips, "top_zones": [ "Madhapur", "Gachibowli", "Banjara Hills" ],"peak_hours": [ "8 AM - 10 AM", "6 PM - 9 PM" ] } }