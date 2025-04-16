from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.session import get_db
from app.schemas import UserResponse as User, UserCreate, UserBase as UserUpdate
from app.models import User as UserModel
from app.core.deps import get_current_active_user
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/me", response_model=User)
async def read_current_user(
    user: UserModel = Depends(get_current_active_user)
):
    """
    Получение информации о текущем пользователе.
    
    Returns:
        User: Информация о текущем пользователе
    """
    return user

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Обновление информации о текущем пользователе.
    
    Args:
        user_update (UserUpdate): Данные для обновления
        db (AsyncSession): Асинхронная сессия базы данных
        current_user (UserModel): Текущий пользователь
    
    Returns:
        User: Обновленная информация о пользователе
    
    Raises:
        HTTPException: Если новый email или username уже заняты
    """
    # Проверка email, если он изменился
    if user_update.email and user_update.email != current_user.email:
        result = await db.execute(
            select(UserModel).where(UserModel.email == user_update.email)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email
    
    # Проверка username, если он изменился
    if user_update.username and user_update.username != current_user.username:
        result = await db.execute(
            select(UserModel).where(UserModel.username == user_update.username)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        current_user.username = user_update.username
    
    # Обновление пароля, если он изменился
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.delete("/me")
async def delete_current_user(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Удаление текущего пользователя.
    
    Args:
        db (AsyncSession): Асинхронная сессия базы данных
        current_user (UserModel): Текущий пользователь
    
    Returns:
        dict: Сообщение об успешном удалении
    """
    await db.delete(current_user)
    await db.commit()
    return {"message": "User successfully deleted"} 