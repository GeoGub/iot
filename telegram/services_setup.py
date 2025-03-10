from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import redis
from typing import Optional, Dict, Any, List
from logger import logger
from settings import settings



class ServiceContainer:
    _instance: Optional['ServiceContainer'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._dispatcher: Optional[Dispatcher] = None
            self._redis: Optional[redis.Redis] = None
            self._bot: Optional[Bot] = None
            self.users: List = [] # TODO: changethis to redis storage
            self._initialized = True

    async def init_redis(self) -> None:
        """Инициализация Redis с обработкой ошибок"""
        if self._redis is not None:
            return

        try:
            self._redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            if not self._redis.ping():
                raise ConnectionError("Redis connection failed")
            logger.info("Redis successfully connected")
        except Exception as e:
            logger.error(f"Redis connection error: {str(e)}")
            self._redis = None
            raise

    async def init_bot(self) -> None:
        """Инициализация бота"""
        if self._bot is None:
            self._bot = Bot(
                token=settings.TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML)
            )
            logger.info("Bot instance created")

    async def init_dispatcher(self) -> None:
        """Инициализация диспетчера"""
        if self._dispatcher is None:
            self._dispatcher = Dispatcher()
            logger.info("Dispatcher initialized")


    @property
    def redis(self) -> redis.Redis:
        if self._redis is None:
            raise RuntimeError("Redis not initialized")
        return self._redis

    @property
    def bot(self) -> Bot:
        if self._bot is None:
            raise RuntimeError("Bot not initialized")
        return self._bot

    @property
    def dispatcher(self) -> Dispatcher:
        if self._dispatcher is None:
            raise RuntimeError("Dispatcher not initialized")
        return self._dispatcher

    def get_services(self) -> Dict[str, Any]:
        """Возвращает словарь с инициализированными сервисами"""
        return {
            'bot': self._bot,
            'dispatcher': self._dispatcher,
            'redis': self._redis
        }
    
    async def shutdown(self) -> None:
        """Корректное завершение работы сервисов"""
        if self._bot:
            await self._bot.session.close()
            logger.info("Bot session closed")
        if self._redis:
            self._redis.close()
            logger.info("Redis connection closed")

# Инициализация контейнера
container = ServiceContainer()

async def init_services():
    """Инициализация всех сервисов"""
    try:
        await container.init_redis()
        await container.init_bot()
        await container.init_dispatcher()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize services: {str(e)}")
        await container.shutdown()
        raise

async def shutdown_services():
    """Корректное завершение работы всех сервисов"""
    await container.shutdown()
    logger.info("All services shutdown completed")

