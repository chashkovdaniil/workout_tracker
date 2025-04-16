from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.session import get_db
from app.models.workout_type import WorkoutType
from app.schemas import WorkoutTypeCreate, WorkoutTypeResponse, WorkoutTypeBase
from app.models.user import User
from app.core.deps import get_current_active_user

router = APIRouter(
    tags=["workout types"],
)

@router.post("/", response_model=WorkoutTypeResponse, status_code=201)
async def create_workout_type(
    workout_type: WorkoutTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создание нового типа тренировки."""
    # Проверяем, существует ли тип тренировки с таким именем у текущего пользователя
    stmt = select(WorkoutType).filter(
        WorkoutType.name == workout_type.name,
        WorkoutType.user_id == current_user.id
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail="Тип тренировки с таким именем уже существует"
        )

    # Создаем новый тип тренировки
    db_workout_type = WorkoutType(
        name=workout_type.name,
        description=workout_type.description,
        user_id=current_user.id
    )
    db.add(db_workout_type)
    await db.commit()
    await db.refresh(db_workout_type)
    return WorkoutTypeResponse(
        id=db_workout_type.id,
        name=db_workout_type.name,
        description=db_workout_type.description,
        created_at=db_workout_type.created_at,
        icon_url=db_workout_type.icon_url,
        user_id=db_workout_type.user_id
    )

@router.get("/", response_model=list[WorkoutTypeResponse])
async def get_workout_types(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение списка типов тренировок."""
    stmt = select(WorkoutType).where(
        WorkoutType.user_id == current_user.id
    ).offset(skip).limit(limit)
    result = await db.execute(stmt)
    workout_types = result.scalars().all()
    
    return [
        WorkoutTypeResponse(
            id=wt.id,
            name=wt.name,
            description=wt.description,
            user_id=wt.user_id
        ) for wt in workout_types
    ]

@router.get("/{workout_type_id}", response_model=WorkoutTypeResponse)
async def get_workout_type(
    workout_type_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение конкретного типа тренировки по ID."""
    stmt = select(WorkoutType).where(
        WorkoutType.id == workout_type_id,
        WorkoutType.user_id == current_user.id
    )
    result = await db.execute(stmt)
    workout_type = result.scalar_one_or_none()
    
    if workout_type is None:
        raise HTTPException(
            status_code=404,
            detail="Тип тренировки не найден"
        )
    
    return WorkoutTypeResponse(
        id=workout_type.id,
        name=workout_type.name,
        description=workout_type.description,
        user_id=workout_type.user_id,
        created_at=workout_type.created_at,
        icon_url=workout_type.icon_url
    )

@router.put("/{workout_type_id}", response_model=WorkoutTypeResponse)
async def update_workout_type(
    workout_type_id: int,
    workout_type_in: WorkoutTypeBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновление типа тренировки."""
    # Получаем тип тренировки
    stmt = select(WorkoutType).where(
        WorkoutType.id == workout_type_id,
        WorkoutType.user_id == current_user.id
    )
    result = await db.execute(stmt)
    workout_type = result.scalar_one_or_none()
    
    if workout_type is None:
        raise HTTPException(
            status_code=404,
            detail="Тип тренировки не найден"
        )
    
    # Проверяем, существует ли другой тип тренировки с таким именем
    if workout_type_in.name != workout_type.name:
        stmt = select(WorkoutType).filter(
            WorkoutType.name == workout_type_in.name,
            WorkoutType.user_id == current_user.id,
            WorkoutType.id != workout_type_id
        )
        result = await db.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=400,
                detail="Тип тренировки с таким именем уже существует"
            )
    
    # Обновляем поля
    for field, value in workout_type_in.dict(exclude_unset=True).items():
        setattr(workout_type, field, value)
    
    await db.commit()
    await db.refresh(workout_type)
    
    return WorkoutTypeResponse(
        id=workout_type.id,
        name=workout_type.name,
        description=workout_type.description,
        user_id=workout_type.user_id,
        created_at=workout_type.created_at,
        icon_url=workout_type.icon_url
    )

@router.delete("/{workout_type_id}")
async def delete_workout_type(
    workout_type_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаление типа тренировки."""
    # Получаем тип тренировки
    stmt = select(WorkoutType).filter(
        WorkoutType.id == workout_type_id,
        WorkoutType.user_id == current_user.id
    )
    result = await db.execute(stmt)
    workout_type = result.scalar_one_or_none()
    
    if workout_type is None:
        raise HTTPException(
            status_code=404,
            detail="Тип тренировки не найден"
        )
    
    # Удаляем тип тренировки
    await db.delete(workout_type)
    await db.commit()
    
    return {"message": "Тип тренировки успешно удален"} 