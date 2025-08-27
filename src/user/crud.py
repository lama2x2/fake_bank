from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.user.models import User


def create_user(db: Session, name: str, email: str, balance: Decimal) -> User:
    user = User(name=name, email=email, balance=balance)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:  # unique email
        db.rollback()
        raise ValueError("email already exists") from exc
    db.refresh(user)
    return user


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)))


def transfer(db: Session, from_user_id: UUID, to_user_id: UUID, amount: Decimal) -> tuple[User, User]:
    if from_user_id == to_user_id:
        raise ValueError("cannot transfer to self")

    # transactional money transfer with row-level locks
    with db.begin():
        from_user = db.execute(
            select(User).where(User.id == from_user_id).with_for_update()
        ).scalar_one_or_none()
        to_user = db.execute(
            select(User).where(User.id == to_user_id).with_for_update()
        ).scalar_one_or_none()

        if from_user is None or to_user is None:
            raise ValueError("user not found")

        if Decimal(from_user.balance) < amount:
            raise ValueError("insufficient funds")

        from_user.balance = Decimal(from_user.balance) - amount
        to_user.balance = Decimal(to_user.balance) + amount

        db.add(from_user)
        db.add(to_user)

    db.refresh(from_user)
    db.refresh(to_user)
    return from_user, to_user


