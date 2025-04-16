from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.session import get_db
from app.models.user import User
from app.schemas import UserBase, UserCreate, UserResponse, Token, TokenData
from app.core.deps import get_current_active_user
from app.core.auth import oauth2_scheme
from jose import jwt, JWTError

router = APIRouter(
    tags=["auth"],
)

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Регистрация нового пользователя.
    
    Args:
        user (UserCreate): Данные для создания пользователя
        db (AsyncSession): Сессия базы данных
    
    Returns:
        User: Созданный пользователь
    
    Raises:
        HTTPException: Если пользователь с таким email уже существует
    """
    # Проверяем, существует ли пользователь с таким email
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Создаем нового пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """
    Аутентификация пользователя и получение токена.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Данные формы аутентификации
        db (AsyncSession): Сессия базы данных
    
    Returns:
        dict[str, str]: Токен доступа и его тип
    
    Raises:
        HTTPException: Если пользователь не найден или пароль неверный
    """
    # Ищем пользователя по email
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    # Создаем токен доступа
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await db.scalar(
        select(User).where(User.username == token_data.username)
    )
    if user is None:
        raise credentials_exception
    return user 