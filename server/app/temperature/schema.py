from pydantic import BaseModel
from abc import ABC

from uuid import UUID

class TemperatureBaseSchema(BaseModel, ABC):
    temperature: float

class TemperatureInSchema(TemperatureBaseSchema):
    pass

class TemperatureOutSchema(TemperatureBaseSchema):
    uuid: UUID
    created_at_timestamp: int

    class Config:
        from_attributes = True
