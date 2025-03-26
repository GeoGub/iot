from sqlmodel.ext.asyncio.session import AsyncSession
from app.shemas.humidity import HumidityFilterSchema
from app.models.humidity import Humidity
from sqlmodel import select


async def get_humidity(
    session: AsyncSession,
    filters: HumidityFilterSchema,
):
    query = (
        select(Humidity)
        .where(
            Humidity.created_at_timestamp >= filters.start_timestamp,
        )
        .where(Humidity.created_at_timestamp <= filters.end_timestamp)
    )
    result = await session.exec(query)
    result = result.all()
    return result


async def get_current_humidity(session: AsyncSession):
    query = (
        select(Humidity)
        .order_by(Humidity.created_at_timestamp.desc())
        .limit(1)
    )
    result = await session.exec(query)
    result = result.one()
    return result
