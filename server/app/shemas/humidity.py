from pydantic import BaseModel, Field
from abc import ABC
from app.schema import CreatedAtToMsConverter, ClimateFilterSchema


class Humidity(BaseModel, ABC):
    humidity: float = Field(gt=0, lt=100)


class HumidityInSchema(Humidity):
    pass


class HumidityOutSchema(Humidity, CreatedAtToMsConverter):
    class Config:
        from_attributes = True


class HumidityFilterSchema(ClimateFilterSchema):
    pass
