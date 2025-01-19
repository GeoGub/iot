from fastapi.routing import APIRouter

from app.temperature.models import Temperature
from app.temperature.schema import TemperatureInSchema, TemperatureOutSchema
from typing import Annotated, List, Dict
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlmodel import select

router = APIRouter(prefix="/temperatures", tags=["temperature"])

@router.post("", responses={
    201: {"description": "Created", "model": TemperatureOutSchema},
}, status_code=201)
async def create_temperature(session: Annotated[AsyncSession, Depends(get_db)], data: TemperatureInSchema):
    temperature = Temperature.model_validate(data)
    session.add(temperature)
    await session.commit()
    await session.refresh(temperature)
    return 201, temperature

@router.get("", responses={
    200: {"description": "OK", "model": Dict[str, List[TemperatureOutSchema]]},
}, status_code=200)
async def get_temperature(session: Annotated[AsyncSession, Depends(get_db)]):
    temperatures = await session.exec(select(Temperature).order_by(Temperature.created_at_timestamp.asc()))
    return {"items": temperatures.all()}
