from pydantic import BaseModel, Field
from enum import Enum
from abc import ABC

from uuid import UUID
import time

class PeriodType(str, Enum):
    days = "days"
    hours = "hours"
    minutes = "minutes"


class TemperatureBaseSchema(BaseModel, ABC):
    temperature: float

class TemperatureInSchema(TemperatureBaseSchema):
    pass

class TemperatureFilterSchema(BaseModel):
    type: PeriodType = PeriodType.days
    start_timestamp: int = Field(default_factory=time.time)

class TemperatureFiteredOutSchema(TemperatureBaseSchema):
    day: str
    temperature: float
    timestamp: int
    hour: int = None
    minute: int = None

    class Config:
        from_attributes = True

class TemperatureOutSchema(TemperatureBaseSchema):
    uuid: UUID
    created_at_timestamp: int

    class Config:
        from_attributes = True
