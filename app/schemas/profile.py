from pydantic import BaseModel, EmailStr


class CreateProfileRequest(BaseModel):
    full_name: str
    email: EmailStr
    profile_photo_url: str | None = None