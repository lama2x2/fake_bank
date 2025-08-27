from fastapi import Header, HTTPException, status

from src.config import settings


async def require_admin(x_admin_token: str | None = Header(default=None, alias="X-Admin-Token")) -> None:
    expected = settings.admin_token
    if not x_admin_token or x_admin_token != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")


