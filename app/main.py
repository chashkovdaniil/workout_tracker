from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.routers import workout, workout_type, exercise, auth, user
from app.core.session import init_db
from app.core.logging import get_logger
from app.core.security import limiter, rate_limit_exceeded_handler

logger = get_logger(__name__)

app = FastAPI(
    title="Workout Tracker API",
    description="API для отслеживания тренировок и упражнений",
    version="1.0.0",
)

# Настройка rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Включаем роутеры
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(workout.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(workout_type.router, prefix="/api/v1/workout-types", tags=["workout types"])
app.include_router(exercise.router, prefix="/api/v1/exercises", tags=["exercises"])

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения."""
    logger.info("Starting up...")
    await init_db()
    logger.info("Database initialized")

@app.get("/")
async def root(request: Request):
    """Корневой эндпоинт."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Workout Tracker API"}

@app.get("/health")
async def health_check(request: Request):
    """Проверка здоровья API."""
    logger.info("Health check performed")
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    ) 