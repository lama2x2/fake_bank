from uuid import uuid4

from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import validates

from src.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    balance = Column(Numeric(12, 2), nullable=False, default=0)

    @validates("email")
    def validate_email(self, key, address):  # noqa: ARG002
        if "@" not in address:
            raise ValueError("invalid email")
        return address.lower()


