from aiogram import Dispatcher
import redis
from settings import settings

def redis_setup():
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD, decode_responses=True)

    try:
        res = redis_client.ping()
        print("PING:", res) # TODO: logging this
    except Exception as e:
        print(e)
        return None

    return redis_client

def dispatcher_setup():
    return Dispatcher()


dp = dispatcher_setup()
redis_client = redis_setup()
