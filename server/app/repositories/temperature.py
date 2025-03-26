from sqlmodel.ext.asyncio.session import AsyncSession
from app.shemas.temperature import TemperatureFilterSchema
from app.models.temperature import Temperature
from sqlmodel import select


async def get_temperature(
    session: AsyncSession,
    filters: TemperatureFilterSchema,
):
    query = (
        select(Temperature)
        .where(
            Temperature.created_at_timestamp >= filters.start_timestamp,
        )
        .where(Temperature.created_at_timestamp <= filters.end_timestamp)
    )
    result = await session.exec(query)
    result = result.all()
    return result


async def get_current_temperature(session: AsyncSession):
    query = (
        select(Temperature)
        .order_by(Temperature.created_at_timestamp.desc())
        .limit(1)
    )
    result = await session.exec(query)
    result = result.one()
    return result
