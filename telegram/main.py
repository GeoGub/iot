import logging
from settings import settings
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.telegram_handlers import router
from handlers.mqtt_handlers import handle_mqtt_message
import asyncio
from services_setup import container, init_services, shutdown_services
import aiomqtt
from logger import logger

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

async def start_mqtt_subscriber():
    logger.info("Connecting to MQTT broker...")
    try:
        async with aiomqtt.Client("192.168.0.111") as client:
            await client.subscribe("result/controller/topic")
            logger.info("Subscribed to MQTT topics")
            
            async for message in client.messages:
                logger.info("Received MQTT message: %s", message.payload)
                if message:
                    await handle_mqtt_message(message.payload.decode("utf-8"))
    except Exception as e:
        logger.error(f"MQTT connection error: {str(e)}")
        raise

async def start_telegram_bot():
    try:
        logger.info("Starting Telegram bot...")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(container.bot)
    except Exception as e:
        logger.error(f"Telegram bot error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
