from sqlmodel import SQLModel, Field

from uuid import UUID, uuid4
import time


class Temperature(SQLModel, table=True):
    uuid: UUID = Field(primary_key=True, default_factory=uuid4)
    created_at_timestamp: int = Field(default_factory=time.time)
    temperature: float
