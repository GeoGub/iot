from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    ENVIROMENT: Literal["local", "staging", "production"] = "local"

    TOKEN: str
    IOT_PASSWORD: str # Пароль для бота чтобы его не могли использовать кто-угодно

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    MQTT_BROKER: str = "localhost"
    MQTT_TOPIC: str = "tasks/controller/topic"

    QUEUE_NAME: str = "task_queue"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
