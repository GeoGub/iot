from pydantic import BaseModel, field_validator, Field
import time


class CreatedAtToMsConverter(BaseModel):
    created_at_timestamp: int = Field(description="Created at timestamp in ms")

    @field_validator("created_at_timestamp", mode="before")
    @classmethod
    def convert_to_ms(cls, value):
        return value * 1000


class ClimateFilterSchema(BaseModel):
    start_timestamp: int | float = Field(
        default_factory=0, description="Start timestamp in ms"
    )
    end_timestamp: int | float = Field(
        default_factory=lambda: int(time.time() * 1000),
        description="End timestamp in ms",
    )

    @field_validator("start_timestamp", "end_timestamp", mode="before")
    @classmethod
    def convert_to_ms(cls, value: int | float):
        return int(value) / 1000
