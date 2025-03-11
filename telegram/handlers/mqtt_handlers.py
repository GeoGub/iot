import json
from typing import Any, Dict

from logger import logger
from settings import settings
from services import BotSingleton, Container, RedisSingleton
from dependency_injector.wiring import inject, Provide


async def handle_mqtt_message(message: str) -> None:
    try:
        message_lower = message.lower()
        if "temperature" in message_lower:
            await _process_sensor_data(message, "get_temperature")
        elif "humidity" in message_lower:
            await _process_sensor_data(message, "get_humidity")
    except Exception as e:
        logger.error(f"Error processing MQTT message: {str(e)}")


async def _process_sensor_data(message: str, sensor_type: str) -> None:
    try:
        tasks = await _get_redis_tasks()
        if not tasks:
            logger.debug("No tasks found in queue")
            return

        processed = 0
        for task_id, task_data in tasks.items():
            if await _process_single_task(
                task_id=task_id,
                task_data=task_data,
                sensor_type=sensor_type,
                message=message,
            ):
                processed += 1

        logger.info(f"Processed {processed}/{len(tasks)} {sensor_type} tasks")

    except Exception as e:
        logger.error(f"Error processing {sensor_type} data: {str(e)}")


@inject
async def _get_redis_tasks(
    redis: RedisSingleton = Provide[Container.redis],
) -> Dict[bytes, bytes]:
    try:
        return redis.hgetall(settings.PROCESSED_QUEUE_NAME)
    except Exception as e:
        logger.error(f"Redis error: {str(e)}")
        return {}


@inject
async def _process_single_task(
    task_id: bytes,
    task_data: bytes,
    sensor_type: str,
    message: str,
    bot: BotSingleton = Provide[Container.bot],
    redis: RedisSingleton = Provide[Container.redis],
) -> bool:
    try:
        task = json.loads(task_data)
        if task.get("task") != sensor_type:
            return False

        user_id = task.get("user_id")
        if not user_id:
            logger.warning(f"Missing user_id in task {task_id}")
            return False

        await bot.send_message(chat_id=user_id, text=message)
        redis.hdel(settings.PROCESSED_QUEUE_NAME, task_id)
        logger.debug(f"Processed task {task_id} for user {user_id}")
        return True

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in task {task_id}")
        await _safe_delete_task(task_id)
        return False
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}")
        return False


async def _safe_delete_task(
    task_id: bytes, redis: RedisSingleton = Provide[Container.redis]
) -> None:
    try:
        redis.hdel(settings.PROCESSED_QUEUE_NAME, task_id)
    except Exception as e:
        logger.error(f"Failed to delete task {task_id}: {str(e)}")
