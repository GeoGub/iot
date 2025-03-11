import time
from typing import ClassVar, Generic, Optional, TypeVar, Tuple

import redis
from aiogram import Bot, Dispatcher
from logger import logger
from settings import settings

# from handlers.mqtt_handlers import handle_mqtt_message
from dependency_injector import providers, containers
from dependency_injector.wiring import inject, Provide

T = TypeVar("T")

MAX_RETRIES = 3


class Singleton(Generic[T]):
    """Базовый Singleton класс"""

    _instance: ClassVar[Optional[T]] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls, *args, **kwargs):
        """Создаем экземпляр класса"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def initialized(self) -> bool:
        """Параметр инициализации класса"""
        return self._initialized


class RedisSingleton(Singleton[redis.Redis], redis.Redis):
    """Класс для работы с Redis"""

    def __init__(
        self,
        *_,
        host: str,
        port: int = 6379,
        db: int = 0,
        password: str = None,
        decode_responses: bool = True,
        **kwargs,
    ):
        """Конструктор класса"""
        if not self._initialized:
            super().__init__(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=decode_responses,
                **kwargs,
            )
            self._initialized = True

    def change_connection(
        self, host: str, port: int = 6379, db: int = 0, password: str = None, **kwargs
    ) -> None:
        """Функция изменения параметров подключения к Redis"""

        self.close()
        self._initialized = False
        self.__init__(host=host, port=port, db=db, password=password, **kwargs)


class UserStorage(Singleton["UserStorage"]):
    def __init__(self, redis: RedisSingleton):
        self.redis = redis
        self.key = "registered_users"

    async def is_registered(self, user_id: int) -> bool:
        return await self.redis.sismember(self.key, user_id)

    async def register(self, user_id: int):
        await self.redis.sadd(self.key, user_id)


class BotSingleton(Singleton[Bot], Bot):
    """Класс для работы с Telegram ботом"""

    def __init__(self, token: str, session=None, default=None, *_, **kwargs) -> None:
        """Конструктор класса"""
        super().__init__(token, session, default, **kwargs)
        self._initialized = True


class Container(containers.DeclarativeContainer):
    redis = providers.Singleton(
        RedisSingleton,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
    bot = providers.Singleton(BotSingleton, token=settings.TELEGRAM_BOT_TOKEN)
    dispatcher = providers.Singleton(Dispatcher)

    user_storage = providers.Singleton(
        lambda redis: UserStorage(redis=redis()),
        redis=redis,
    )


def init_redis(
    *_,
    redis: RedisSingleton = Provide[Container.redis],
    **kwargs,
) -> redis.Redis:
    """Функция инициализации Redis"""

    try:
        redis.ping()
        logger.info("Redis connected")
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        raise ConnectionError from e
    return redis


async def init_bot(*_, bot: BotSingleton = Provide[Container.bot], **kwargs) -> Bot:
    """Функция инициализации Telegram бота"""

    try:
        await bot.get_me()
        logger.info("Bot connected")
    except Exception as e:
        logger.error(f"Bot connection error: {e}")
        raise ConnectionError from e
    return bot


def init_dispatcher(
    *_, dispatcher: Dispatcher = Provide[Container.dispatcher], **kwargs
) -> Dispatcher:
    """Функция инициализации Telegram диспатчера"""

    dispatcher = Dispatcher(**kwargs)
    return dispatcher


async def init_services() -> Tuple[RedisSingleton, BotSingleton, Dispatcher]:
    """Функция инициализации сервисов"""

    redis = None
    bot = None
    dispatcher = None
    for _ in range(MAX_RETRIES):
        if not redis:
            try:
                redis = init_redis()
            except ConnectionError as e:
                pass
        if not bot:
            try:
                bot = await init_bot()
            except ConnectionError as e:
                pass
        if not dispatcher:
            try:
                dispatcher = init_dispatcher()
            except ConnectionError as e:
                pass
        if not all((redis, bot, dispatcher)):
            time.sleep(5)
            continue
        break
    logger.info("Services initialized successfully")
    return redis, bot, dispatcher
