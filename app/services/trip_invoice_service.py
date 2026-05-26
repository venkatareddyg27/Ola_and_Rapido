import uuid

from decimal import Decimal

from sqlalchemy import select

from sqlalchemy.orm import (
    selectinload
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.trips import Trip

from app.models.trip_invoices import (
    TripInvoice
)

from app.models.user_models import (
    DriverProfile
)

from app.core.enums import (
    PaymentStatus,
    InvoiceStatus,
    TripType
)

from app.utils.pdf_generator import (
    PDFInvoiceService
)


class TripInvoiceService:

    @staticmethod
    async def generate_invoice(
        db: AsyncSession,
        trip_id
    ):

        # =============================================
        # GET TRIP
        # =============================================

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
                Trip.id == trip_id
            )

        )

        trip = result.scalars().first()

        # =============================================
        # TRIP NOT FOUND
        # =============================================

        if not trip:

            raise Exception(
                "Trip not found"
            )

        # =============================================
        # CHECK EXISTING INVOICE
        # =============================================

        existing_invoice_result = await db.execute(

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
                TripInvoice.trip_id
                == trip.id
            )

        )

        existing_invoice = (

            existing_invoice_result
            .scalars()
            .first()

        )

        # =============================================
        # RETURN EXISTING INVOICE
        # =============================================

        if existing_invoice:

            return existing_invoice

        # =============================================
        # BASE FARE
        # =============================================

        base_fare = Decimal("50.00")

        # =============================================
        # DISTANCE
        # =============================================

        estimated_distance = Decimal(

            str(
                trip.estimated_distance or 0
            )

        )

        # =============================================
        # DISTANCE CHARGE
        # =============================================

        distance_charge = (

            estimated_distance
            * Decimal("12")

        )

        # =============================================
        # OTHER CHARGES
        # =============================================

        duration_minutes = 0

        time_charge = Decimal("0")

        waiting_charge = Decimal("0")

        surge_charge = Decimal("0")

        discount_amount = Decimal("0")

        # =============================================
        # SUBTOTAL
        # =============================================

        subtotal = (

            base_fare

            + distance_charge

            + waiting_charge

            + surge_charge

            + time_charge

        )

        # =============================================
        # TAX
        # =============================================

        tax_amount = (
            subtotal * Decimal("0.05")
        )

        # =============================================
        # TOTAL AMOUNT
        # =============================================

        total_amount = (

            subtotal

            + tax_amount

            - discount_amount

        )

        # =============================================
        # GENERATE INVOICE NUMBER
        # =============================================

        invoice_number = (

            f"INV-"
            f"{uuid.uuid4().hex[:10].upper()}"

        )

        # =============================================
        # TRIP TYPE
        # =============================================

        trip_type = (

            TripType.PARCEL

            if getattr(
                trip,
                "is_parcel",
                False
            )

            else TripType.ride

        )

        # =============================================
        # CREATE INVOICE
        # =============================================

        invoice = TripInvoice(

            trip_id=trip.id,

            customer_id=trip.customer_id,

            driver_id=trip.driver_id,

            vehicle_id=None,

            invoice_number=invoice_number,

            trip_type=trip_type,

            base_fare=base_fare,

            distance_km=estimated_distance,

            distance_charge=distance_charge,

            duration_minutes=duration_minutes,

            time_charge=time_charge,

            waiting_charge=waiting_charge,

            surge_charge=surge_charge,

            tax_amount=tax_amount,

            discount_amount=discount_amount,

            subtotal=subtotal,

            total_amount=total_amount,

            payment_method="cash",

            payment_status=PaymentStatus.SUCCESS,

            invoice_status=InvoiceStatus.generated

        )

        # =============================================
        # SAVE INVOICE
        # =============================================

        db.add(invoice)

        await db.commit()

        await db.refresh(invoice)

        # =============================================
        # RELOAD RELATIONSHIPS
        # =============================================

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

        # =============================================
        # GENERATE PDF
        # =============================================

        pdf_path = (

            PDFInvoiceService
            .generate_invoice_pdf(
                invoice
            )

        )

        # =============================================
        # SAVE PDF URL
        # =============================================

        invoice.pdf_url = pdf_path

        await db.commit()

        await db.refresh(invoice)

        # =============================================
        # RETURN INVOICE
        # =============================================

        return invoice