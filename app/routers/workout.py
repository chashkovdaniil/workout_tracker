from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.session import get_db
from app.schemas.workout import WorkoutCreate, WorkoutResponse
from app.models.workout import Workout
from app.models.user import User
from app.core.deps import get_current_active_user

router = APIRouter(
    tags=["workouts"],
)

@router.post("/", response_model=WorkoutResponse, status_code=201)
async def create_workout(
    workout: WorkoutCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Workout:
    """
    Создает новую тренировку.

    Args:
        workout (WorkoutCreate): Данные для создания тренировки
        db (AsyncSession): Сессия базы данных
        current_user (User): Текущий пользователь

    Returns:
        Workout: Созданная тренировка

    Raises:
        HTTPException: Если тренировка с таким именем уже существует
    """
    # Проверяем, существует ли тренировка с таким именем у текущего пользователя
    stmt = select(Workout).where(
        Workout.name == workout.name,
        Workout.user_id == current_user.id
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Тренировка с таким именем уже существует"
        )

    # Создаем новую тренировку
    db_workout = Workout(
        name=workout.name,
        description=workout.description,
        workout_type_id=workout.workout_type_id,
        user_id=current_user.id
    )
    db.add(db_workout)
    await db.commit()
    await db.refresh(db_workout)
    return db_workout

@router.get("/", response_model=list[WorkoutResponse])
async def get_workouts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[Workout]:
    """
    Возвращает список всех тренировок текущего пользователя.

    Args:
        db (AsyncSession): Сессия базы данных
        current_user (User): Текущий пользователь

    Returns:
        list[Workout]: Список тренировок
    """
    stmt = select(Workout).where(Workout.user_id == current_user.id)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(workout_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получение тренировки по ID.
    
    Args:
        workout_id (int): ID тренировки
        db (AsyncSession): Асинхронная сессия базы данных
    
    Returns:
        Workout: Тренировка
    
    Raises:
        HTTPException: Если тренировка не найдена
    """
    result = await db.execute(select(Workout).where(Workout.id == workout_id))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return workout

@router.put("/{workout_id}", response_model=WorkoutResponse)
async def update_workout(workout_id: int, workout: WorkoutCreate, db: AsyncSession = Depends(get_db)):
    """
    Обновление тренировки.
    
    Args:
        workout_id (int): ID тренировки для обновления
        workout (WorkoutCreate): Данные для обновления
        db (AsyncSession): Асинхронная сессия базы данных
    
    Returns:
        Workout: Обновленная тренировка
    
    Raises:
        HTTPException: Если тренировка не найдена
    """
    result = await db.execute(select(Workout).where(Workout.id == workout_id))
    db_workout = result.scalar_one_or_none()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    
    for key, value in workout.dict(exclude_unset=True).items():
        setattr(db_workout, key, value)
    
    await db.commit()
    await db.refresh(db_workout)
    return db_workout

@router.delete("/{workout_id}")
async def delete_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """
    Удаляет тренировку по ID.

    Args:
        workout_id (int): ID тренировки
        workout_id (int): ID тренировки для удаления
        db (AsyncSession): Асинхронная сессия базы данных
    
    Returns:
        dict: Сообщение об успешном удалении
    
    Raises:
        HTTPException: Если тренировка не найдена
    """
    result = await db.execute(select(Workout).where(Workout.id == workout_id))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    
    await db.delete(workout)
    await db.commit()
    return {"message": "Тренировка успешно удалена"} 