from fastapi.routing import APIRouter

from app.models.temperature import Temperature
from app.shemas.temperature import (
    TemperatureInSchema,
    TemperatureOutSchema,
    TemperatureFilterSchema,
)
from typing import Annotated, List
from fastapi import Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_db
from app.repositories.temperature import (
    get_temperature as get_temperature_repository,
    get_current_temperature as get_current_temperature_repository,
)


router = APIRouter(prefix="/temperature", tags=["temperature"])


@router.post(
    "",
    responses={
        201: {"description": "Created", "model": TemperatureOutSchema},
    },
    status_code=201,
)
async def create_temperature(
    session: Annotated[AsyncSession, Depends(get_db)],
    data: TemperatureInSchema,
):
    # Вынести в сервис
    temperature = Temperature.model_validate(data)
    session.add(temperature)
    await session.commit()
    await session.refresh(temperature)
    return 201, temperature


@router.get(
    "",
    response_model=List[TemperatureOutSchema],
    responses={
        200: {"description": "OK", "model": List[TemperatureOutSchema]},
    },
    status_code=200,
)
async def get_temperature(
    session: Annotated[AsyncSession, Depends(get_db)],
    filters: TemperatureFilterSchema = Query(...),
):
    return await get_temperature_repository(session, filters)


@router.get("/current")
async def get_current_temperature(
    session: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_current_temperature_repository(session)
