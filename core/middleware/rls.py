from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from core.config import settings
from core.database import execute_transaction

class RLSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization:
            try:
                token = authorization.split()[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                tenant_id = payload.get("tenant_id")
                if tenant_id:
                    await execute_transaction(
                        "SET LOCAL tenant_id = $1",
                        tenant_id
                    )
                    response = await call_next(request)
                    return response
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
        return await call_next(request)
