from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.enums import (PaymentStatus,InvoiceStatus,TripType)

class TripInvoiceResponse(BaseModel):

    id: UUID

    trip_id: UUID

    invoice_number: str

    trip_type: TripType

    customer_name: str | None = None

    driver_name: str | None = None

    vehicle_number: str | None = None

    base_fare: Decimal

    distance_km: Decimal

    distance_charge: Decimal

    duration_minutes: int

    time_charge: Decimal

    waiting_charge: Decimal

    surge_charge: Decimal

    tax_amount: Decimal

    discount_amount: Decimal

    subtotal: Decimal

    total_amount: Decimal

    payment_method: str | None = None

    payment_status: PaymentStatus

    invoice_status: InvoiceStatus

    pdf_url: str | None = None

    generated_at: datetime

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )