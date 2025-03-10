import redis
import time
import paho.mqtt.client as mqtt
import json
import logging
import signal
import sys

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Конфигурация
REDIS_CONFIG = {'host': '192.168.0.111', 'port': 6379, 'db': 0}
MQTT_CONFIG = {
    'host': '192.168.0.111',
    'port': 1883,
    'keepalive': 60,
    'topic': 'tasks/controller/topic'
}

class TaskProcessor:
    def __init__(self):
        self.running = True
        self.redis = redis.Redis(**REDIS_CONFIG)
        self.mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._setup_signals()

    def _setup_signals(self):
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

    def graceful_shutdown(self, *args):
        logger.info("Shutting down...")
        self.running = False
        self.mqtt.disconnect()
        sys.exit(0)

    def connect_mqtt(self):
        while self.running:
            try:
                self.mqtt.connect(MQTT_CONFIG['host'], MQTT_CONFIG['port'], MQTT_CONFIG['keepalive'])
                self.mqtt.loop_start()
                logger.info("Connected to MQTT broker")
                return
            except Exception as e:
                logger.error(f"MQTT error: {e}, retrying in 5s...")
                time.sleep(5)

    def process_tasks(self):
        while self.running:
            try:
                cursor = 0
                while True:
                    cursor, data = self.redis.hscan("task_queue", cursor, count=100)
                    if not data:
                        time.sleep(1)
                        break
                    
                    for task_id, value in data.items():
                        self._process_task(task_id, value)
                    
                    if cursor == 0:
                        break
            except redis.RedisError as e:
                logger.error(f"Redis error: {e}")
                time.sleep(5)

    def _process_task(self, task_id, task_bytes):
        try:
            task = json.loads(task_bytes)
            self.mqtt.publish(MQTT_CONFIG['topic'], task.get("task"))
            self.redis.hdel("task_queue", task_id)
            self.redis.hset("processed_tasks", task_id, task_bytes)
            logger.info(f"Processed task {task_id}")
        except json.JSONDecodeError:
            logger.error(f"Invalid task format: {task_id}")
            self.redis.hdel("task_queue", task_id)
        except Exception as e:
            logger.error(f"Failed to process task {task_id}: {e}")

if __name__ == "__main__":
    processor = TaskProcessor()
    processor.connect_mqtt()
    processor.process_tasks()