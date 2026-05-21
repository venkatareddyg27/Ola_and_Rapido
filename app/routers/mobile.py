from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.user_services import otp_service
from app.schemas.user_schemas import SendOTPRequest, VerifyOTPRequest

router = APIRouter(
    prefix="/otp",
    tags=["mobile auth"],
)

@router.post("/send")
async def send_otp(
    request: SendOTPRequest,
    db: AsyncSession = Depends(get_db),
):
    return await otp_service.send_otp(
        request.mobile_number,
        db,
    )


@router.post("/verify")
async def verify_otp(
    request: VerifyOTPRequest,
    db: AsyncSession = Depends(get_db),
):
    return await otp_service.verify_otp(
        request.mobile_number,
        request.otp,
        db,
    )


@router.post("/resend")
async def resend_otp(
    request: SendOTPRequest,
    db: AsyncSession = Depends(get_db),
):
    return await otp_service.resend_otp(
        request.mobile_number,
        db,
    )