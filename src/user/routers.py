from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db
from src.utils.permissions import require_admin
from src.utils.auth import require_jwt
from src.user import crud
from src.user.schemas import UserCreate, UserOut, TransferRequest


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_user(db, payload.name, payload.email, Decimal(payload.balance))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_jwt)])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await crud.list_users(db)


transfer_router = APIRouter(tags=["transfer"])


@transfer_router.post("/transfer", status_code=status.HTTP_200_OK)
async def make_transfer(
    payload: TransferRequest,
    claims: dict = Depends(require_jwt),
    db: AsyncSession = Depends(get_db),
):
    # только владелец from_user_id может инициировать перевод
    subject = claims.get("sub")
    if subject is None or str(payload.from_user_id) != str(subject):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
    try:
        from_user, to_user = await crud.transfer(
            db,
            payload.from_user_id,
            payload.to_user_id,
            Decimal(payload.amount),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {
        "from_user": UserOut.model_validate(from_user),
        "to_user": UserOut.model_validate(to_user),
    }


