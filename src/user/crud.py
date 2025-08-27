from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User


async def create_user(db: AsyncSession, name: str, email: str, balance: Decimal) -> User:
    user = User(name=name, email=email, balance=balance)
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:  # unique email
        await db.rollback()
        raise ValueError("email already exists") from exc
    await db.refresh(user)
    return user


async def list_users(db: AsyncSession) -> list[User]:
    result = await db.scalars(select(User).order_by(User.id))
    return list(result)


async def transfer(db: AsyncSession, from_user_id: UUID, to_user_id: UUID, amount: Decimal) -> tuple[User, User]:
    if from_user_id == to_user_id:
        raise ValueError("cannot transfer to self")

    # transactional money transfer with row-level locks
    async with db.begin():
        from_user = (
            await db.execute(
                select(User).where(User.id == from_user_id).with_for_update()
            )
        ).scalar_one_or_none()
        to_user = (
            await db.execute(
                select(User).where(User.id == to_user_id).with_for_update()
            )
        ).scalar_one_or_none()

        if from_user is None or to_user is None:
            raise ValueError("user not found")

        if Decimal(from_user.balance) < amount:
            raise ValueError("insufficient funds")

        from_user.balance = Decimal(from_user.balance) - amount
        to_user.balance = Decimal(to_user.balance) + amount

        db.add(from_user)
        db.add(to_user)

    await db.refresh(from_user)
    await db.refresh(to_user)
    return from_user, to_user


