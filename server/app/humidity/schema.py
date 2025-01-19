from pydantic import BaseModel, Field
from abc import ABC
from uuid import UUID

class Humidity(BaseModel, ABC):
    humidity: float = Field(gt=0, lt=100)

class HumidityInSchema(Humidity):
    pass

class HumidityOutSchema(Humidity):
    uuid: UUID
    created_at_timestamp: int

    class Config:
        from_attributes = True
