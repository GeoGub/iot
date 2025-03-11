from sqlmodel import SQLModel, Field

import time


class SoundLevel(SQLModel, table=True):
    created_at_timestamp: int = Field(
        primary_key=True, default_factory=lambda: int(time.time())
    )
    sound_level: int
