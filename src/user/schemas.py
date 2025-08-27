from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    balance: Decimal = Field(default=0, ge=0)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    balance: Decimal

    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: Decimal = Field(gt=0)


