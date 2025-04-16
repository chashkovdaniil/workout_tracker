# Workout Tracker API

API для отслеживания тренировок, упражнений и прогресса.

## Содержание

- [Установка](#установка)
- [Переменные окружения](#переменные-окружения)
- [Запуск](#запуск)
- [API Endpoints](#api-endpoints)
- [Развертывание](#развертывание)
- [Тестирование](#тестирование)
- [Миграции базы данных](#миграции-базы-данных)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/chashkovdaniil/workout_tracker.git
cd workout_tracker
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
.\venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Переменные окружения

Создайте файл `.env` в корневой директории проекта со следующими переменными:

```env
# База данных
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/workout_tracker

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Настройки приложения
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=Workout Tracker
```

## Запуск

1. Убедитесь, что PostgreSQL запущен и доступен
2. Примените миграции:
```bash
alembic upgrade head
```
3. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## API Endpoints

### Аутентификация

- `POST /api/v1/auth/register` - Регистрация нового пользователя
- `POST /api/v1/auth/login` - Вход в систему
- `GET /api/v1/auth/me` - Получение информации о текущем пользователе

### Типы тренировок

- `POST /api/v1/workout-types/` - Создание нового типа тренировки
- `GET /api/v1/workout-types/` - Получение списка типов тренировок
- `GET /api/v1/workout-types/{id}` - Получение типа тренировки по ID
- `PUT /api/v1/workout-types/{id}` - Обновление типа тренировки
- `DELETE /api/v1/workout-types/{id}` - Удаление типа тренировки

### Упражнения

- `POST /api/v1/exercises/` - Создание нового упражнения
- `GET /api/v1/exercises/` - Получение списка упражнений
- `GET /api/v1/exercises/{id}` - Получение упражнения по ID
- `PUT /api/v1/exercises/{id}` - Обновление упражнения
- `DELETE /api/v1/exercises/{id}` - Удаление упражнения

### Тренировки

- `POST /api/v1/workouts/` - Создание новой тренировки
- `GET /api/v1/workouts/` - Получение списка тренировок
- `GET /api/v1/workouts/{id}` - Получение тренировки по ID
- `PUT /api/v1/workouts/{id}` - Обновление тренировки
- `DELETE /api/v1/workouts/{id}` - Удаление тренировки

## Развертывание

### Docker

1. Соберите Docker образ:
```bash
docker build -t workout-tracker .
```

2. Запустите контейнер:
```bash
docker run -d \
  --name workout-tracker \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:password@db:5432/workout_tracker \
  -e SECRET_KEY=your-secret-key-here \
  workout-tracker
```

### Kubernetes

1. Создайте namespace:
```bash
kubectl create namespace workout-tracker
```

2. Примените конфигурации:
```bash
kubectl apply -f k8s/
```

## Тестирование

Запустите тесты:
```bash
pytest tests/ -v
```

## Миграции базы данных

1. Создание новой миграции:
```bash
alembic revision --autogenerate -m "description of changes"
```

2. Применение миграций:
```bash
alembic upgrade head
```

3. Откат миграции:
```bash
alembic downgrade -1
``` 