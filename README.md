# Workout Tracker API

API для отслеживания тренировок, упражнений и прогресса.

## Содержание

- [Установка](#установка)
- [Переменные окружения](#переменные-окружения)
- [Запуск](#запуск)
- [Документация API (Swagger UI)](#документация-api-swagger-ui)
- [Развертывание](#развертывание)
- [Тестирование](#тестирование)
- [Миграции базы данных](#миграции-базы-данных)
- [Сборка и публикация Docker-образа](#сборка-и-публикация-docker-образа)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/chashkovdaniil/workout_tracker.git
cd workout_tracker
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv 
source venv/bin/activate  # для Linux/Mac
# или для Windows:
# .\venv\Scripts\activate 
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Переменные окружения

Создайте файл `.env` в корневой директории проекта (`backend/.env`) со следующими переменными. Пример можно найти в `.env.example`.

```env
# База данных PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/workout_tracker

# Настройки JWT токенов
SECRET_KEY=your_very_secret_strong_key_here_please_change_it
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 
# REFRESH_TOKEN_EXPIRE_DAYS=7 # Если используется refresh token

# Настройки приложения
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME="Workout Tracker API"

# Для инициализации первого суперпользователя (опционально, если есть скрипт)
# FIRST_SUPERUSER_EMAIL=admin@example.com
# FIRST_SUPERUSER_USERNAME=admin
# FIRST_SUPERUSER_PASSWORD=yoursecurepassword
```
**Примечание:** Убедитесь, что `SECRET_KEY` является криптографически стойким ключом.

## Запуск

1. Убедитесь, что PostgreSQL запущен и доступен по `DATABASE_URL`.
2. Примените миграции базы данных (если они еще не применены):
```bash
alembic upgrade head
```
3. Запустите приложение с помощью Uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
    Флаг `--reload` удобен для разработки. Для продуктивного режима его следует убрать.

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## Документация API (Swagger UI)

Актуальная интерактивная документация API (Swagger UI) доступна после запуска приложения.
Перейдите по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

Схема OpenAPI в формате JSON доступна по адресу: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

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

## Сборка и публикация Docker-образа

1. **Сборка образа:**

    Для сборки образа с указанием версии и тега `latest` для платформы `linux/amd64` (замените `YOUR_REGISTRY_PATH` и `VERSION`):
    ```bash
    docker buildx build --platform linux/amd64 -t YOUR_REGISTRY_PATH/workout_tracker:VERSION -t YOUR_REGISTRY_PATH/workout_tracker:latest .
    ```
    Пример для Yandex Container Registry:
    ```bash
    docker buildx build --platform linux/amd64 -t cr.yandex/crphu341kkj0m3tqrul1/workout_tracker:0.0.12 -t cr.yandex/crphu341kkj0m3tqrul1/workout_tracker:latest .
    ```

2. **Аутентификация в Docker Registry (например, Yandex Container Registry):**

    Если вы еще не аутентифицированы, выполните:
    ```bash
    yc container registry configure-docker
    ```
    Или используйте Docker-токен (замените `YOUR_IAM_TOKEN`):
    ```bash
    docker login --username iam --password YOUR_IAM_TOKEN cr.yandex
    ```

3. **Отправка (push) образов в Docker Registry:**

    Замените `YOUR_REGISTRY_PATH` и `VERSION`:
    ```bash
    docker push YOUR_REGISTRY_PATH/workout_tracker:VERSION
    docker push YOUR_REGISTRY_PATH/workout_tracker:latest
    ```
    Пример для Yandex Container Registry:
    ```bash
    docker push cr.yandex/crphu341kkj0m3tqrul1/workout_tracker:0.0.12
    docker push cr.yandex/crphu341kkj0m3tqrul1/workout_tracker:latest
    ``` 