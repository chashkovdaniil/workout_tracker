from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.session import get_db
from app.models.exercise import Exercise
from app.schemas import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.models.user import User
from app.core.deps import get_current_active_user

router = APIRouter(
    tags=["exercises"],
)

@router.post("/", response_model=ExerciseResponse, status_code=201)
async def create_exercise(
    exercise: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Exercise:
    """
    Создает новое упражнение.

    Args:
        exercise (ExerciseCreate): Данные для создания упражнения
        db (AsyncSession): Сессия базы данных
        current_user (User): Текущий пользователь

    Returns:
        Exercise: Созданное упражнение

    Raises:
        HTTPException: Если упражнение с таким именем уже существует
    """
    # Проверяем, существует ли упражнение с таким именем у текущего пользователя
    stmt = select(Exercise).where(
        Exercise.name == exercise.name,
        Exercise.user_id == current_user.id
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Упражнение с таким именем уже существует"
        )

    # Создаем новое упражнение
    db_exercise = Exercise(
        name=exercise.name,
        description=exercise.description,
        muscle_groups=exercise.muscle_groups,
        user_id=current_user.id
    )
    db.add(db_exercise)
    await db.commit()
    await db.refresh(db_exercise)
    return db_exercise

@router.get("/", response_model=list[ExerciseResponse])
async def get_exercises(
    skip: int = 0,
    limit: int = 100,
    muscle_groups: list[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение списка упражнений с пагинацией и фильтрацией."""
    # Базовый запрос для упражнений текущего пользователя
    stmt = select(Exercise).where(Exercise.user_id == current_user.id)
    
    # Добавляем фильтрацию по группам мышц, если указаны
    if muscle_groups:
        stmt = stmt.where(Exercise.muscle_groups.overlap(muscle_groups))
    
    # Добавляем пагинацию
    stmt = stmt.offset(skip).limit(limit)
    
    # Выполняем запрос
    result = await db.execute(stmt)
    exercises = result.scalars().all()
    
    return [
        ExerciseResponse(
            id=ex.id,
            name=ex.name,
            description=ex.description,
            muscle_groups=ex.muscle_groups,
            user_id=ex.user_id
        ) for ex in exercises
    ]

@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить упражнение по ID."""
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    )
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    exercise_in: ExerciseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить упражнение."""
    # Получаем упражнение
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    )
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Обновляем поля упражнения
    for field, value in exercise_in.dict(exclude_unset=True).items():
        setattr(exercise, field, value)
    
    await db.commit()
    await db.refresh(exercise)
    return exercise

@router.delete("/{exercise_id}", status_code=200)
async def delete_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """
    Удаляет упражнение по ID.

    Args:
        exercise_id (int): ID упражнения
        db (AsyncSession): Сессия базы данных
        current_user (User): Текущий пользователь

    Returns:
        dict[str, str]: Сообщение об успешном удалении

    Raises:
        HTTPException: Если упражнение не найдено или не принадлежит текущему пользователю
    """
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.user_id == current_user.id
    )
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()
    
    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Упражнение не найдено"
        )

    await db.delete(exercise)
    await db.commit()
    
    return {"message": "Упражнение успешно удалено"} 