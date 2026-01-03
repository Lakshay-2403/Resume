from pydantic import BaseModel

class SendOTPRequest(BaseModel):
    identifier: str
    is_email: bool  # True for email, False for mobile

class VerifyOTPRequest(BaseModel):
    identifier: str
    otp: str

class ResendOTPRequest(BaseModel):
    identifier: str

class OTPResponse(BaseModel):
    message: str