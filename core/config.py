from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://goverdhan:GUifedChKLzAgLlH31zgLPMdWdu5jk6H@dpg-cu8cr0ij1k6c739tdnog-a.oregon-postgres.render.com/stockitdb_v656"
    SECRET_KEY: str = "c5a48de7190fe947d007b1b2256ac27ab4b110fb2840ac0a7d4cbbd4676e88d2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
