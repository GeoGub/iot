from fastapi.routing import APIRouter

from app.humidity.models import Humidity
from app.humidity.schema import HumidityInSchema, HumidityOutSchema
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db


router = APIRouter(prefix="/humidities", tags=["humidity"])

@router.post("", responses={
    201: {"description": "Created", "model": HumidityOutSchema},
}, status_code=201)
async def create_humidity(session: Annotated[AsyncSession, Depends(get_db)], data: HumidityInSchema):
    humidity = Humidity.model_validate(data)
    session.add(humidity)
    await session.commit()
    await session.refresh(humidity)
    return humidity
