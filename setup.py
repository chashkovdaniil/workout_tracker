from setuptools import setup, find_packages

setup(
    name="workout_tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "pydantic==2.6.1",
        "python-dotenv==1.0.1",
        "sqlalchemy[asyncio]==2.0.25",
        "asyncpg==0.29.0",
        "alembic==1.13.1",
        "python-multipart==0.0.6",
        "pytest==7.4.4",
        "httpx==0.26.0",
        "pytest-asyncio==0.23.5",
        "pytest-cov==4.1.0",
        "pydantic-settings==2.1.0",
        "slowapi==0.1.9",
        "email-validator==2.1.0",
        "passlib[bcrypt]==1.7.4",
        "python-jose[cryptography]==3.3.0",
    ],
) 