from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.temperature.api import router as temperature_router
from app.humidity.api import router as humidity_router
from app.sound_level.api import router as sound_level_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Укажите URL вашего клиента
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP-методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(temperature_router)
app.include_router(humidity_router)
app.include_router(sound_level_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
