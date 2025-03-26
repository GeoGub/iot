import asyncio

import aiomqtt
import handlers
import handlers.mqtt_handlers
import handlers.telegram_handlers
import services
from aiogram import Dispatcher
from dependency_injector.wiring import Provide, inject
from handlers.mqtt_handlers import handle_mqtt_message
from logger import logger
from services import (
    BotSingleton,
    Container,
    RedisSingleton,
    init_services,
)
from settings import settings


async def start_mqtt_subscriber():
    logger.info("Connecting to MQTT broker...")
    try:
        async with aiomqtt.Client(settings.MQTT_BROKER) as client:
            await client.subscribe("result/controller/topic")
            logger.info("Subscribed to MQTT topics")

            async for message in client.messages:
                logger.info("Received MQTT message: %s", message.payload)
                if message:
                    await handle_mqtt_message(message.payload.decode("utf-8"))
    except Exception as e:
        logger.error(f"MQTT connection error: {str(e)}")
        raise


@inject
async def start_telegram_bot(
    bot: BotSingleton = Provide[Container.bot],
    dp: Dispatcher = Provide[Container.dispatcher],
):
    try:
        logger.info("Starting Telegram bot...")
        dp.include_router(handlers.telegram_handlers.router)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Telegram bot error: {str(e)}")
        raise


@inject
async def shutdown_services(
    redis: RedisSingleton = Provide[Container.redis],
    bot: BotSingleton = Provide[Container.bot],
) -> None:
    """Функция завершения работы сервисов"""

    if redis.initialized:
        redis.close()
    # if bot.initialized:
    #     await bot.close()


async def main():
    try:
        logger.info("Starting application initialization...")
        await init_services()
        logger.info("Services initialized successfully")

        asyncio.create_task(start_mqtt_subscriber())
        logger.info("MQTT subscriber task created")

        await start_telegram_bot()
        logger.info("Telegram bot started successfully")
    except Exception as e:
        logger.critical(f"Application failed: {str(e)}")
        raise
    finally:
        logger.info("Shutting down application...")
        await shutdown_services()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(
        modules=[__name__, handlers.telegram_handlers, handlers.mqtt_handlers, services]
    )
    asyncio.run(main())
