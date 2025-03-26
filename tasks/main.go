package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/go-redis/redis/v8"
	"golang.org/x/net/context"
)

const (
	redisAddr  = "192.168.0.111:6379"
	mqttBroker = "tcp://192.168.0.111:1883"
	mqttTopic  = "tasks/controller/topic"
	taskQueue  = "task_queue"
)

var (
	ctx         = context.Background()
	redisClient *redis.Client
	mqttClient  mqtt.Client
)

func init() {
	// Настройка Redis
	redisClient = redis.NewClient(&redis.Options{
		Addr: redisAddr,
		DB:   0,
	})

	// Настройка MQTT
	opts := mqtt.NewClientOptions().AddBroker(mqttBroker)
	mqttClient = mqtt.NewClient(opts)
	if token := mqttClient.Connect(); token.Wait() && token.Error() != nil {
		log.Fatalf("Ошибка подключения к MQTT: %v", token.Error())
	}
}

func processTasks() {
	for {
		tasks, err := redisClient.HGetAll(ctx, taskQueue).Result()
		if err != nil {
			log.Printf("Ошибка получения задач из Redis: %v", err)
			continue
		}

		for key, value := range tasks {
			var task map[string]string
			if err := json.Unmarshal([]byte(value), &task); err != nil {
				log.Printf("Ошибка разбора JSON: %v", err)
				continue
			}

			if taskMsg, ok := task["task"]; ok {
				mqttClient.Publish(mqttTopic, 0, false, taskMsg)
				redisClient.HDel(ctx, taskQueue, key)
				fmt.Printf("Опубликовано в MQTT: %s\n", taskMsg)
			}
		}

		time.Sleep(1 * time.Second)
	}
}

func main() {
	processTasks()
}
