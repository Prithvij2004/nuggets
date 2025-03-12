from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid
from pydantic import EmailStr
from sqlmodel import VARCHAR, Column, SQLModel, Field

class Users(SQLModel, table=True):
    __tablename__ = "users" #type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    google_id: str = Field(unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True))
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate":lambda: datetime.now(timezone.utc)},
        nullable=False
    )

class Notes(SQLModel, table=True):
    __tablename__ = "notes" #type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    content: str = Field(nullable=False, index=True)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate":lambda: datetime.now(timezone.utc)},
        nullable=False
    )
