import uuid
from datetime import datetime
from enum import StrEnum
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TransactionType(StrEnum):
    U2U = "u2u"
    TOP_UP = "top-up"
    LLM = "llm"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int] = mapped_column()

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(sa.ForeignKey("users.id"))
    transaction_type: Mapped[TransactionType] = mapped_column(sa.Enum(TransactionType))
    value: Mapped[int] = mapped_column()
    properties: Mapped[dict] = mapped_column(sa.JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())

    user: Mapped["User"] = relationship(back_populates="transactions")

    def __repr__(self) -> str:
        return f"Transaction(id={self.id}, type={self.transaction_type}, value={self.value})"
