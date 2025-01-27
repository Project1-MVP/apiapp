from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://goverdhan:RHw65M5S5f7xK0kgWulKfZ7oMNRX0AKd@dpg-cub6969opnds73egpoog-a.singapore-postgres.render.com/stockitdb_ja4l"
    SECRET_KEY: str = "c5a48de7190fe947d007b1b2256ac27ab4b110fb2840ac0a7d4cbbd4676e88d2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = b'xqQEZjgpWTYxITQPiyc80hgPaoxPCJefTtA/ucgRATA='

settings = Settings()
