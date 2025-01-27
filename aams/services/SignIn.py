from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import pyotp
from core.config import settings
from cryptography.fernet import Fernet


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    fernet = Fernet(settings.ENCRYPTION_KEY)

    @staticmethod
    def create_totp_secret():
        plain_secret = pyotp.random_base32()
        return AuthService.fernet.encrypt(plain_secret.encode()).decode()

    @staticmethod
    def get_totp_provisioning_url(username: str, encrypted_secret: str):
        plain_secret = AuthService.fernet.decrypt(encrypted_secret.encode()).decode()
        totp = pyotp.TOTP(plain_secret)
        return totp.provisioning_uri(username, issuer_name="StockIT")

    @staticmethod
    def verify_totp(encrypted_secret: str, code: str, valid_window: int = 1):
        plain_secret = AuthService.fernet.decrypt(encrypted_secret.encode()).decode()
        totp = pyotp.TOTP(plain_secret)
        return totp.verify(code, valid_window=valid_window)

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)
