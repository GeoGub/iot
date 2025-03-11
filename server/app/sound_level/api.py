from fastapi.routing import APIRouter

from app.sound_level.models import SoundLevel
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

router = APIRouter(prefix="/sound-levels", tags=["sound_level"])


@router.post("")
async def create_sound_level(
    session: Annotated[AsyncSession, Depends(get_db)], data: dict
):
    sound_level = SoundLevel.model_validate(data)
    session.add(sound_level)
    await session.commit()
    await session.refresh(sound_level)
    return 201, sound_level
