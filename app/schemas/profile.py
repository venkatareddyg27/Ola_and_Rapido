from pydantic import BaseModel, EmailStr


class CreateProfileRequest(BaseModel):
    full_name: str
    email: EmailStr
    gender: str
    profile_photo_url: str | None = None