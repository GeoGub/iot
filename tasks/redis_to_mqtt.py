import redis
import time
import paho.mqtt.client as mqtt
import json

# Настройки Redis
redis_client = redis.Redis(host='192.168.0.111', port=6379, db=0)

# Настройки MQTT
MQTT_BROKER = "192.168.0.111"  # Укажите IP, если брокер на другом сервере
MQTT_TOPIC = "tasks/controller/topic"
MQTT_RESULT = "result/controller/topic"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Обновленная версия API
client.connect(MQTT_BROKER, 1883, 60)

def process_tasks():
    while True:
        tasks = redis_client.hgetall("task_queue")
        for key, value in tasks.items():
            task = json.loads(value)
            client.publish(MQTT_TOPIC, task.get("task"))
            redis_client.hdel("task_queue", key)
        time.sleep(1)  # Если задач нет, ждём 1 секунду

if __name__ == "__main__":
    process_tasks()
