from pydantic import BaseModel, EmailStr

class TenantRegistration(BaseModel):
    business_name: str
    phone_number: str
    email: EmailStr
    username: str
    password: str

class UserRegistration(BaseModel):
    username: str
    password: str
    phone_number: str
    email: EmailStr
    role: str = "user"

class TOTPVerification(BaseModel):
    username: str
    totp_code: str

class Login(BaseModel):
    username: str
    password: str
    totp_code: str

class ForgotPassword(BaseModel):
    username: str
    totp_code: str
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
