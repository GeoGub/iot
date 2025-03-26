from pydantic import BaseModel
from enum import Enum
from abc import ABC
from app.schema import CreatedAtToMsConverter, ClimateFilterSchema


class PeriodType(str, Enum):
    days = "days"
    hours = "hours"
    minutes = "minutes"


class TemperatureBaseSchema(BaseModel, ABC):
    temperature: float


class TemperatureInSchema(TemperatureBaseSchema):
    pass


class TemperatureOutSchema(TemperatureBaseSchema, CreatedAtToMsConverter):
    class Config:
        from_attributes = True


class TemperatureFilterSchema(ClimateFilterSchema):
    pass
