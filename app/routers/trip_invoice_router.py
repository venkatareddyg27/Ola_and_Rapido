from fastapi import (APIRouter,Depends,HTTPException,status)
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import (selectinload)
from sqlalchemy.ext.asyncio import (AsyncSession)
from app.core.database import get_db
from app.core.security import (get_current_user)
from app.models.user_models import (User,DriverProfile)
from app.models.trips import Trip
from app.models.trip_invoices import (TripInvoice)
from app.schemas.trip_invoice import (TripInvoiceResponse)
from app.services.trip_invoice_service import (TripInvoiceService)


router = APIRouter(
    prefix="/trip-invoices",
    tags=["Trip Invoices"])


@router.post(
    "/generate",
    response_model=TripInvoiceResponse)
async def generate_trip_invoice(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )):

    try:

        result = await db.execute(

            select(Trip)

            .options(

                selectinload(
                    Trip.customer
                ),

                selectinload(
                    Trip.driver
                ).selectinload(
                    DriverProfile.user
                )

            )

            .where(
                Trip.customer_id
                == current_user.id
            )

            .where(
                Trip.status == "COMPLETED"
            )

            .order_by(
                Trip.created_at.desc()
            )

        )

        trip = result.scalars().first()

        if not trip:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="No completed trip found"

            )

        invoice = await (
            TripInvoiceService.generate_invoice(
                db=db,
                trip_id=trip.id
            )
        )

        invoice_result = await db.execute(

            select(TripInvoice)

            .options(

                selectinload(
                    TripInvoice.customer
                ),

                selectinload(
                    TripInvoice.driver
                ).selectinload(
                    DriverProfile.user
                ),

                selectinload(
                    TripInvoice.vehicle
                )

            )

            .where(
                TripInvoice.id
                == invoice.id
            )

        )

        invoice = (
            invoice_result
            .scalars()
            .first()
        )

        return {

            "id": invoice.id,

            "trip_id": invoice.trip_id,

            "invoice_number": (invoice.invoice_number),

            "trip_type": (invoice.trip_type),

            "customer_name": (

                invoice.customer.full_name

                if invoice.customer

                else None

            ),

            "driver_name": (

                invoice.driver.user.full_name

                if invoice.driver
                and invoice.driver.user

                else None

            ),

            "vehicle_number": (

                invoice.vehicle.vehicle_number

                if invoice.vehicle

                else None

            ),

            "base_fare": invoice.base_fare,

            "distance_km": invoice.distance_km,

            "distance_charge": invoice.distance_charge,

            "duration_minutes": invoice.duration_minutes,

            "time_charge": invoice.time_charge,

            "waiting_charge": invoice.waiting_charge,

            "surge_charge": invoice.surge_charge,

            "tax_amount": invoice.tax_amount,

            "discount_amount": invoice.discount_amount,

            "subtotal": invoice.subtotal,

            "total_amount": invoice.total_amount,

            "payment_method": invoice.payment_method,

            "payment_status": invoice.payment_status,

            "invoice_status": invoice.invoice_status,

            "pdf_url": invoice.pdf_url,

            "generated_at": invoice.generated_at,

            "created_at": invoice.created_at,

            "updated_at": invoice.updated_at

        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(e)

        )


@router.get(
    "/latest",
    response_model=TripInvoiceResponse)
async def get_latest_invoice(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )):

    try:

        result = await db.execute(

            select(TripInvoice)

            .options(

                selectinload(
                    TripInvoice.customer
                ),

                selectinload(
                    TripInvoice.driver
                ).selectinload(
                    DriverProfile.user
                ),

                selectinload(
                    TripInvoice.vehicle
                )

            )

            .where(
                TripInvoice.customer_id
                == current_user.id
            )

            .order_by(
                TripInvoice.created_at.desc()
            )

        )

        invoice = result.scalars().first()

        if not invoice:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Invoice not found"

            )

        return {

            "id": invoice.id,

            "trip_id": invoice.trip_id,

            "invoice_number": (invoice.invoice_number),

            "trip_type": (invoice.trip_type),

            "customer_name": (

                invoice.customer.full_name

                if invoice.customer

                else None

            ),

            "driver_name": (

                invoice.driver.user.full_name

                if invoice.driver
                and invoice.driver.user

                else None

            ),

            "vehicle_number": (

                invoice.vehicle.vehicle_number

                if invoice.vehicle

                else None

            ),

            "base_fare": invoice.base_fare,

            "distance_km": invoice.distance_km,

            "distance_charge": invoice.distance_charge,

            "duration_minutes": invoice.duration_minutes,

            "time_charge": invoice.time_charge,

            "waiting_charge": invoice.waiting_charge,

            "surge_charge": invoice.surge_charge,

            "tax_amount": invoice.tax_amount,

            "discount_amount": invoice.discount_amount,

            "subtotal": invoice.subtotal,

            "total_amount": invoice.total_amount,

            "payment_method": invoice.payment_method,

            "payment_status": invoice.payment_status,

            "invoice_status": invoice.invoice_status,

            "pdf_url": invoice.pdf_url,

            "generated_at": invoice.generated_at,

            "created_at": invoice.created_at,

            "updated_at": invoice.updated_at

        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(e)

        )


@router.get(
    "/download")
async def download_latest_invoice(

    db: AsyncSession = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )):

    try:

        result = await db.execute(

            select(TripInvoice)

            .where(
                TripInvoice.customer_id
                == current_user.id
            )

            .order_by(
                TripInvoice.created_at.desc()
            )

        )

        invoice = result.scalars().first()

        if not invoice:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Invoice not found"

            )

        if not invoice.pdf_url:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Invoice PDF not found"

            )

        return FileResponse(

            path=invoice.pdf_url,

            media_type="application/pdf",

            filename=(
                f"{invoice.invoice_number}.pdf"
            )

        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(e)

        )