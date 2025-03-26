from sqlmodel import Field, SQLModel

import time


class Humidity(SQLModel, table=True):
    created_at_timestamp: int = Field(
        primary_key=True, default_factory=lambda: int(time.time())
    )
    humidity: float
