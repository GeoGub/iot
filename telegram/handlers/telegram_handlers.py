from aiogram import Router, F, types
from settings import settings
import time
import json
from services_setup import container
from logger import logger

router = Router()

@router.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет, я бот для управления домом. Чтобы продолжить работу - введи код подтверждения")
    

@router.message(F.text == "/get_temperature")
async def get_temperature(message: types.Message):
    if message.from_user.id not in container.users:
        await message.answer("Вы не зарегистрированы")
        return
    container.redis.hset(name=settings.QUEUE_NAME, key=str(time.time()), value=json.dumps({'task': "get_temperature", "user_id": message.from_user.id}))
    await message.answer("Я вас услышал. Получаю данные...")


@router.message(F.text)
async def register(message: types.Message):
    logger.info("Text received: %s", message.text)
    if not message.from_user.id in container.users:
        if message.text == settings.PASSWORD:
            container.users.append(message.from_user.id)
            await message.answer("Вы зарегистрированы")
            return
        await message.answer("Неправильный пароль")
        return
    await message.answer("Вы уже зарегистрированы")
