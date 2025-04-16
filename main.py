from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import workout, workout_type, exercise, auth, user
from app.database.session import init_db

app = FastAPI(
    title="Workout Tracker API",
    description="API для отслеживания тренировок и упражнений",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Включение роутеров
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(workout.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(workout_type.router, prefix="/api/v1/workout-types", tags=["workout-types"])
app.include_router(exercise.router, prefix="/api/v1/exercises", tags=["exercises"])

@app.on_event("startup")
async def startup_event():
    """
    Инициализация базы данных при запуске приложения.
    """
    await init_db()

@app.get("/")
async def root():
    """
    Корневой эндпоинт API.
    
    Returns:
        dict: Приветственное сообщение
    """
    return {"message": "Добро пожаловать в Workout Tracker API"}

@app.get("/health")
async def health_check():
    """
    Эндпоинт для проверки работоспособности API.
    
    Returns:
        dict: Статус API
    """
    return {"status": "healthy"} 