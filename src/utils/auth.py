from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import settings


_bearer = HTTPBearer(auto_error=False)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    now = datetime.now(tz=timezone.utc)
    to_encode: Dict[str, Any] = {"sub": subject, "iat": int(now.timestamp())}
    expire = now + (expires_delta or timedelta(hours=1))
    to_encode["exp"] = int(expire.timestamp())
    token = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token


def verify_jwt_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    return payload


async def require_jwt(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> Dict[str, Any]:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing bearer token")
    return verify_jwt_token(credentials.credentials)


