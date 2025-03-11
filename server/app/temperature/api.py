from fastapi.routing import APIRouter

from app.temperature.models import Temperature
from app.temperature.schema import (
    TemperatureInSchema,
    TemperatureOutSchema,
    TemperatureFilterSchema,
    PeriodType,
    TemperatureFiteredOutSchema,
)
from typing import Annotated, List
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlmodel import select, func, Integer
from datetime import datetime, UTC
from sqlalchemy.sql import extract, text


router = APIRouter(prefix="/temperatures", tags=["temperature"])


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
    temperature = Temperature.model_validate(data)
    session.add(temperature)
    await session.commit()
    await session.refresh(temperature)
    return 201, temperature


@router.get(
    "",
    response_model=List[TemperatureFiteredOutSchema],
    responses={
        200: {"description": "OK", "model": List[TemperatureFiteredOutSchema]},
    },
    status_code=200,
)
async def get_temperature(
    session: Annotated[AsyncSession, Depends(get_db)],
    filters: TemperatureFilterSchema = Query(...),
):
    if filters.type == PeriodType.days:
        query = (
            select(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ).label("day"),
                func.avg(Temperature.temperature).label("temperature"),
            )
            .group_by("day")
            .order_by("day")
        )
    elif filters.type == PeriodType.hours:
        query = (
            select(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ).label("day"),
                extract(
                    "hour", func.to_timestamp(Temperature.created_at_timestamp)
                )
                .cast(Integer)
                .label("hour"),
                func.avg(Temperature.temperature).label("temperature"),
            )
            .group_by(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ),
                extract(
                    "hour", func.to_timestamp(Temperature.created_at_timestamp)
                ),
            )
            .order_by(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ),
                extract(
                    "hour", func.to_timestamp(Temperature.created_at_timestamp)
                ),
            )
        )
    elif filters.type == PeriodType.minutes:
        query = (
            select(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ).label("day"),
                extract(
                    "hour", func.to_timestamp(Temperature.created_at_timestamp)
                )
                .cast(Integer)
                .label("hour"),
                extract(
                    "minute",
                    func.to_timestamp(Temperature.created_at_timestamp),
                )
                .cast(Integer)
                .label("minute"),
                func.avg(Temperature.temperature).label("temperature"),
            )
            .group_by(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ),
                extract(
                    "hour", func.to_timestamp(Temperature.created_at_timestamp)
                ),
                extract(
                    "minute",
                    func.to_timestamp(Temperature.created_at_timestamp),
                ),
            )
            .order_by(
                func.to_char(
                    func.to_timestamp(Temperature.created_at_timestamp),
                    text("'YYYY-MM-DD'"),
                ),
                extract(
                    "hour", func.to_timestamp(Temperature.created_at_timestamp)
                ),
                extract(
                    "minute",
                    func.to_timestamp(Temperature.created_at_timestamp),
                ),
            )
        )
    temperatures = await session.exec(query)
    temperatures = temperatures.mappings().all()
    res = []
    for temperature in temperatures:
        res_temperature = dict(temperature)
        res_temperature["timestamp"] = datetime(
            *map(int, temperature["day"].split("-")),
            hour=temperature.get("hour", 0),
            minute=temperature.get("minute", 0),
            tzinfo=UTC,
        ).timestamp()
        res.append(res_temperature)
    return sorted(res, key=lambda x: x["timestamp"])
