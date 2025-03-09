from aiogram import Router, F, types
from services_setup import redis_client
from settings import settings
import time
import json

router = Router()

@router.message(F.text == "/get_temperature")
async def get_temperature(message: types.Message):
    res = redis_client.hset(name=settings.QUEUE_NAME, key=str(time.time()), value=json.dumps({'task': "get_temperature", "user_id": message.from_user.id}))
    await message.answer("Задача отправлена в очередь")