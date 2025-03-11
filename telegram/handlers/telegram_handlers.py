import json
import time

from aiogram import F, Router, types
from dependency_injector.wiring import Provide, inject
from logger import logger
from services import Container, RedisSingleton, UserStorage
from settings import settings

router = Router()


@router.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(
        "Привет, я бот для управления домом."
        "Чтобы продолжить работу - введи код подтверждения"
    )


@router.message(F.text == "/get_temperature")
@router.message(F.text == "/get_humidity")
@inject
async def get_temperature(
    message: types.Message, redis: RedisSingleton = Provide[Container.redis]
):
    # if not user_storage.is_registered(message.from_user.id):
    #     await message.answer("Вы не зарегистрированы")
    #     return
    redis.hset(
        name=settings.QUEUE_NAME,
        key=str(time.time()),
        value=json.dumps({"task": message.text[1:], "user_id": message.from_user.id}),
    )
    await message.answer("Я вас услышал. Получаю данные...")


@router.message(F.text)
async def register(
    message: types.Message,
    user_storage: UserStorage = Provide[Container.user_storage],
):
    logger.info("Text received: %s", message.text)
    if message.from_user.id not in user_storage.is_registered(message.from_user.id):
        if message.text == settings.PASSWORD:
            user_storage.register(message.from_user.id)
            await message.answer("Вы зарегистрированы")
            return
        await message.answer("Неправильный пароль")
        return
    await message.answer("Вы уже зарегистрированы")
