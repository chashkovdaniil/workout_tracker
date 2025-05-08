from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.security import verify_password
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserInDB
from app.core.auth import oauth2_scheme
from typing import Optional

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Получение текущего пользователя из JWT токена.
    
    Args:
        db (AsyncSession): Сессия базы данных
        token (str): JWT токен
    
    Returns:
        User: Объект пользователя
    
    Raises:
        HTTPException: Если токен недействителен или пользователь не найден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print('payload', payload.get("sub"))
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    
    stmt = select(User).filter(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Получение текущего активного пользователя.
    
    Args:
        current_user (User): Текущий пользователь
    
    Returns:
        User: Активный пользователь
    
    Raises:
        HTTPException: Если пользователь неактивен
    """
    ss: str = current_user.email
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 