from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from app.models.Rent_vehicles import (RentedVehicle,VehicleDamageReport,VehicleAvailability)
from app.models.vehicles import (VehicleDocument,VehiclePhoto)
from app.schemas.Rented_Vehicles import (RentedVehicleCreate,RentedVehicleUpdate,RentalInspectionCreate,RentedVehicleAvailabilityCreate,RentedVehicleDamageReportCreate)
from app.models.rentals import RentalInspection
from app.models.user_models import User
from datetime import datetime

class RentedVehicleService:

    @staticmethod
    async def create_vehicle(
        payload: RentedVehicleCreate,
        current_user: User,
        db: AsyncSession):

        existing_vehicle = await db.execute(
            select(RentedVehicle).where(
                RentedVehicle.registration_number
                == payload.registration_number
            )
        )

        existing_vehicle = (
            existing_vehicle.scalars().first()
        )

        if existing_vehicle:

            raise HTTPException(
                status_code=400,
                detail="Vehicle already exists"
            )

        vehicle = RentedVehicle(

            owner_id=current_user.id,

            make=payload.make,

            model=payload.model,

            year=payload.year,

            registration_number=
            payload.registration_number,

            category=payload.category,

            colour=payload.colour,

            sitting_capacity=
            payload.sitting_capacity,

            fuel_type=payload.fuel_type,

            transmission_type=
            payload.transmission_type,

            fuel_capacity=
            payload.fuel_capacity,

            mileage=payload.mileage,

            current_odometer=
            payload.current_odometer,

            price_per_hour=
            payload.price_per_hour,

            price_per_day=
            payload.price_per_day,

            security_deposit=
            payload.security_deposit,

            ac_available=
            payload.ac_available,

            gps_enabled=
            payload.gps_enabled,

            bluetooth_available=
            payload.bluetooth_available,

            music_system=
            payload.music_system,

            sunroof=
            payload.sunroof,

            airbags=
            payload.airbags,

            boot_space=
            payload.boot_space,

            city=payload.city,

            state=payload.state
        )

        db.add(vehicle)

        await db.commit()

        await db.refresh(vehicle)

        return vehicle



    @staticmethod
    async def get_vehicle(
        vehicle_id: UUID,
        db: AsyncSession):

        result = await db.execute(
            select(RentedVehicle).where(
                RentedVehicle.id == vehicle_id
            )
        )

        vehicle = result.scalars().first()

        if not vehicle:

            raise HTTPException(
                status_code=404,
                detail="Vehicle not found"
            )

        return vehicle


    @staticmethod
    async def update_vehicle(
        vehicle_id: UUID,
        payload: RentedVehicleUpdate,
        current_user: User,
        db: AsyncSession):

        vehicle = await (
            RentedVehicleService.get_vehicle(
                vehicle_id,
                db
            )
        )

        if vehicle.owner_id != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="Unauthorized"
            )

        update_data = payload.dict(
            exclude_unset=True
        )

        for key, value in update_data.items():

            setattr(vehicle, key, value)

        await db.commit()

        await db.refresh(vehicle)

        return vehicle


    @staticmethod
    async def delete_vehicle(
        vehicle_id: UUID,
        current_user: User,
        db: AsyncSession):

        vehicle = await (
            RentedVehicleService.get_vehicle(
                vehicle_id,
                db
            )
        )

        if vehicle.owner_id != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="Unauthorized"
            )

        await db.delete(vehicle)

        await db.commit()

        return {
            "message":
            "Vehicle deleted successfully"
        }


class VehiclePhotoService:


    @staticmethod
    async def upload_vehicle_photo(
        vehicle_id: UUID,
        angle: str,
        file: UploadFile,
        db: AsyncSession):

        file_url = (
            f"/uploads/vehicles/"
            f"{file.filename}"
        )

        photo = VehiclePhoto(

            vehicle_id=vehicle_id,

            photo_url=file_url,

            angle=angle
        )

        db.add(photo)

        await db.commit()

        await db.refresh(photo)

        return photo


class VehicleDocumentService:


    @staticmethod
    async def upload_document(
        vehicle_id: UUID,
        document_type: str,
        file: UploadFile,
        db: AsyncSession
    ):

        file_url = (
            f"/uploads/documents/"
            f"{file.filename}"
        )

        document = VehicleDocument(

            vehicle_id=vehicle_id,

            document_type=document_type,

            document_url=file_url,

            verification_status="pending"
        )

        db.add(document)

        await db.commit()

        await db.refresh(document)

        return document


class VehicleDamageService:


    @staticmethod
    async def create_damage_report(
        payload: RentedVehicleDamageReportCreate,
        current_user: User,
        db: AsyncSession):

        report = VehicleDamageReport(

            vehicle_id=payload.vehicle_id,

            reported_by=current_user.id,

            damage_type=payload.damage_type,

            description=payload.description,

            estimated_repair_cost=
            payload.estimated_repair_cost
        )

        db.add(report)

        await db.commit()

        await db.refresh(report)

        return report


class VehicleAvailabilityService:


    @staticmethod
    async def add_availability(
        payload: RentedVehicleAvailabilityCreate,
        db: AsyncSession):

        availability = VehicleAvailability(

            vehicle_id=payload.vehicle_id,

            available_from=
            payload.available_from,

            available_to=
            payload.available_to
        )

        db.add(availability)

        await db.commit()

        await db.refresh(availability)

        return availability


class RentalInspectionService:


    @staticmethod
    async def create_inspection(
        payload: RentalInspectionCreate,
        current_user: User,
        db: AsyncSession):

        inspection = RentalInspection(

            rental_id=payload.rental_id,

            inspection_type=
            payload.inspection_type,

            fuel_level=
            payload.fuel_level,

            odometer_reading=
            payload.odometer_reading,

            damage_notes=
            payload.damage_notes,

            photo_urls=
            payload.photo_urls,

            video_url=
            payload.video_url,

            inspector_user_id=
            current_user.id,

            inspected_at=datetime.utcnow()
        )

        db.add(inspection)

        await db.commit()

        await db.refresh(inspection)

        return inspection

