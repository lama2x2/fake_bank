from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    balance: Decimal = Field(default=0, ge=0)


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    balance: Decimal

    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    amount: Decimal = Field(gt=0)


