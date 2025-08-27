from fastapi import status, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from uuid import UUID
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.config import settings
from app.schemas.authentification import TokenPayload
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User, Role
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentification/login")

def _create_token(*, sub: str, minutes: int, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(minutes=minutes)
    payload = {
        "sub": sub,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expiration_time.timestamp())
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(user_id: UUID) -> str :
    return _create_token(
        sub=str(user_id),
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        token_type="access"
    )

def create_refresh_token(user_id: UUID) -> str :
    return _create_token(
        sub=str(user_id),
        minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60,
        token_type="refresh"
    )


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    data = decode_token(token)
    if data.type != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user = db.get(User, UUID(data.sub))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or missing user")
    return user

def require_roles(*allowed: Role):
    async def _guard(user: Annotated[User, Depends(get_current_user)]) -> User:
        if allowed and user.user_role not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _guard
