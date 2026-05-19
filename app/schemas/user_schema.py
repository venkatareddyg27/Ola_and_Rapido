from pydantic import BaseModel, Field

class SendOTPRequest(BaseModel):
    mobile_number: str

class VerifyOTPRequest(BaseModel):
    mobile_number: str
    otp: str