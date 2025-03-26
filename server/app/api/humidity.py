from fastapi.routing import APIRouter

from app.models.humidity import Humidity
from app.shemas.humidity import (
    HumidityInSchema,
    HumidityOutSchema,
    HumidityFilterSchema,
)
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.repositories.humidity import (
    get_humidity as get_humidity_repository,
    get_current_humidity as get_current_humidity_repository,
)
from typing import List
from fastapi import Query


router = APIRouter(prefix="/humidity", tags=["humidity"])


@router.post(
    "",
    responses={
        201: {"description": "Created", "model": HumidityOutSchema},
    },
    status_code=201,
)
async def create_humidity(
    session: Annotated[AsyncSession, Depends(get_db)], data: HumidityInSchema
):
    humidity = Humidity.model_validate(data)
    session.add(humidity)
    await session.commit()
    await session.refresh(humidity)
    return humidity


@router.get(
    "",
    response_model=List[HumidityOutSchema],
    responses={
        200: {"description": "OK", "model": List[HumidityOutSchema]},
    },
    status_code=200,
)
async def get_humidity(
    session: Annotated[AsyncSession, Depends(get_db)],
    filters: HumidityFilterSchema = Query(...),
):
    return await get_humidity_repository(session, filters)


@router.get("/current")
async def get_current_humidity(
    session: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_current_humidity_repository(session)
