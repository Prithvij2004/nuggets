from typing import Any, Dict
import uuid
from pydantic import EmailStr
from sqlmodel import VARCHAR, Column, SQLModel, Field

class Users(SQLModel, table=True):
    __table_args__: Dict[str, Any] = {"schema": "public"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    google_id: str = Field(unique=True, nullable=False)
    full_name: str = Field(nullable=False)
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True))
