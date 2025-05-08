from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from typing import List
from app.database.session import get_db
from app.models.workout_exercise import WorkoutExercise
from app.models.workout_type import WorkoutType
from app.models.workout_set import WorkoutSet
from app.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutUpdate
from app.models.workout import Workout
from app.models.user import User
from app.core.deps import get_current_active_user
from app.schemas.workout_exercise import WorkoutExercise as WorkoutExerciseResponse
from app.schemas.workout_exercise import WorkoutExerciseCreate, WorkoutExerciseUpdate

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
    result = await db.execute(select(Workout).where(Workout.user_id == current_user.id)
                                .options(
                                  selectinload(Workout.exercises).selectinload(WorkoutExercise.sets),
                                  selectinload(Workout.exercises).selectinload(WorkoutExercise.exercise),
                                  selectinload(Workout.exercises).selectinload(WorkoutExercise.workout)
                              )
                              .options(selectinload(Workout.workout_type).selectinload(WorkoutType.workouts)))
    return list(result.scalars().all())

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
    result = await db.execute(select(Workout).where(Workout.id == workout_id)
                              .options(
                                  selectinload(Workout.exercises).selectinload(WorkoutExercise.sets),
                                  selectinload(Workout.exercises).selectinload(WorkoutExercise.exercise),
                              )
                              .options(selectinload(Workout.workout_type)))
    
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return workout

@router.patch("/{workout_id}", response_model=WorkoutResponse)
async def update_workout(workout_id: int, workout: WorkoutUpdate, db: AsyncSession = Depends(get_db)):
    """
    Обновление тренировки.
    
    Args:
        workout_id (int): ID тренировки для обновления
        workout (WorkoutUpdate): Данные для обновления
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
        if value is None:
            continue
        if key == "exercises":
            processed_exercise_ids = set()
            new_exercises_for_workout = []

            if value:
                for exercise_payload_data in value:
                    exercise_id = exercise_payload_data.id

                    if exercise_id is not None:
                        processed_exercise_ids.add(exercise_id)
                        updated_we = await update_workout_exercise(
                            workout_id=workout_id,
                            workout_exercise_id=exercise_id,
                            workout_exercise_data=exercise_payload_data,
                            db=db
                        )
                        new_exercises_for_workout.append(updated_we)
                    else:
                        pass
            
        else:
            setattr(db_workout, key, value)
    
    await db.commit()
    result = await db.execute(
        select(Workout)
        .options(
            selectinload(Workout.exercises).selectinload(WorkoutExercise.sets),
            selectinload(Workout.exercises).selectinload(WorkoutExercise.exercise),
            selectinload(Workout.workout_type)
        )
        .where(Workout.id == db_workout.id)
    )
    db_workout = result.scalar_one_or_none()
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


@router.delete("/{workout_id}/exercises/{workout_exercise_id}")
async def delete_workout_exercise(
    workout_exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """
    Удаляет упражнение из тренировки по ID.

    Args:
        workout_exercise_id (int): ID упражнения
        db (AsyncSession): Асинхронная сессия базы данных
    
    Returns:
        dict: Сообщение об успешном удалении
    
    Raises:
        HTTPException: Если тренировка не найдена
    """
    result = await db.execute(select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id))
    workout_exercise = result.scalar_one_or_none()
    if not workout_exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    
    await db.delete(workout_exercise)
    await db.commit()
    return {"message": "Упражнение успешно удалено"} 

@router.post("/{workout_id}/exercises", response_model=WorkoutExerciseResponse)
async def create_workout_exercise(
    workout_id: int,
    workout_exercise_data: WorkoutExerciseCreate,
    db: AsyncSession = Depends(get_db)
):
    db_workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=workout_exercise_data.exercise_id,
        notes=workout_exercise_data.notes
    )

    if workout_exercise_data.sets:
        # Эта часть требует вашей конкретной логики для создания WorkoutSet объектов
        # и добавления их к db_workout_exercise.sets
        # Например:
        # from app.models.workout_set import WorkoutSet # Убедитесь, что модель импортирована
        # for set_create_data in workout_exercise_data.sets:
        #     new_set = WorkoutSet(**set_create_data.dict())
        #     # SQLAlchemy автоматически свяжет new_set с db_workout_exercise при добавлении в коллекцию,
        #     # если cascade настроен правильно, или вы можете установить workout_exercise_id вручную
        #     # после того, как db_workout_exercise получит ID (после flush/commit).
        #     # Более безопасный подход - создать сеты после того, как db_workout_exercise получит ID.
        #     db_workout_exercise.sets.append(new_set) # Если 'sets' это InstrumentedList
        pass


    db.add(db_workout_exercise)
    await db.commit()
    
    created_id = db_workout_exercise.id 

    stmt = (
        select(WorkoutExercise)
        .options(
            selectinload(WorkoutExercise.sets),      
            selectinload(WorkoutExercise.exercise)   
        )
        .where(WorkoutExercise.id == created_id)
    )
    result = await db.execute(stmt)
    final_workout_exercise = result.scalar_one_or_none()

    if not final_workout_exercise:
        raise HTTPException(status_code=500, detail="Не удалось получить созданное упражнение для тренировки")

    return final_workout_exercise


@router.put("/{workout_id}/exercises/{workout_exercise_id}", response_model=WorkoutExerciseResponse)
async def update_workout_exercise(
    workout_id: int, # ID тренировки из пути (для проверки принадлежности)
    workout_exercise_id: int,
    workout_exercise_data: WorkoutExerciseUpdate, # Данные для обновления
    db: AsyncSession = Depends(get_db)
):
    # 1. Получаем существующий WorkoutExercise из базы
    # Загружаем сразу с существующими сетами, чтобы было с чем сравнивать
    stmt_get = (
        select(WorkoutExercise)
        .options(selectinload(WorkoutExercise.sets)) # Загружаем сеты сразу
        .where(WorkoutExercise.id == workout_exercise_id)
    )
    result = await db.execute(stmt_get)
    db_workout_exercise = result.scalar_one_or_none()

    if not db_workout_exercise:
        raise HTTPException(status_code=404, detail=f"Упражнение в тренировке с ID {workout_exercise_id} не найдено")

    # 1.1 Проверяем принадлежность к тренировке из пути (опционально, но рекомендуется)
    if db_workout_exercise.workout_id != workout_id:
        raise HTTPException(status_code=403, detail="Упражнение не принадлежит указанной тренировке")

    # 2. Обновляем прямые атрибуты WorkoutExercise
    update_data_dict = workout_exercise_data.dict(exclude_unset=True)

    if 'exercise_id' in update_data_dict:
        db_workout_exercise.exercise_id = update_data_dict['exercise_id']
    if 'notes' in update_data_dict:
        db_workout_exercise.notes = update_data_dict['notes']

    # 3. Обновляем сеты (sets)
    if workout_exercise_data.sets is not None:
        current_db_sets_map = {s.id: s for s in db_workout_exercise.sets}
        input_set_ids_processed = set()

        new_sets_for_workout_exercise = []

        for set_data_from_input in workout_exercise_data.sets:
            input_set_id = set_data_from_input.id

            if input_set_id is not None:
                input_set_ids_processed.add(input_set_id)
                if input_set_id in current_db_sets_map:
                    # Обновляем существующий сет
                    db_set_to_update = current_db_sets_map[input_set_id]
                    if set_data_from_input.weight is not None:
                        db_set_to_update.weight = set_data_from_input.weight
                    if set_data_from_input.reps is not None:
                        db_set_to_update.reps = set_data_from_input.reps
                    if set_data_from_input.set_number is not None:
                        db_set_to_update.set_number = set_data_from_input.set_number
                    # Если set_number не пришел, он не обновляется
                    new_sets_for_workout_exercise.append(db_set_to_update)
                else:
                    # Сет с таким ID пришел в запросе, но его нет в базе у этого WorkoutExercise
                    # Пропускаем или выбрасываем ошибку, как обсуждалось ранее
                    pass 
            else:
                # Создаем новый сет (ID не указан)
                if set_data_from_input.set_number is None:
                    # Если set_number не предоставлен для нового сета, это ошибка, так как он NOT NULL
                    # Можно автоматически присвоить следующий номер, если есть такая логика,
                    # или требовать от клиента.
                    # Для примера, выбросим ошибку, если не передан для нового сета.
                    raise HTTPException(status_code=422, detail=f"Поле 'set_number' обязательно для новых подходов (сетов). Входные данные для сета: {set_data_from_input.dict()}")
                
                new_db_set = WorkoutSet(
                    workout_exercise_id=db_workout_exercise.id,
                    weight=set_data_from_input.weight if set_data_from_input.weight is not None else 0, # Пример значения по умолчанию, если weight тоже может быть None
                    reps=set_data_from_input.reps if set_data_from_input.reps is not None else 0, # Пример значения по умолчанию
                    set_number=set_data_from_input.set_number # Здесь он уже не None из-за проверки выше
                )
                new_sets_for_workout_exercise.append(new_db_set)

        # Удаляем сеты, которые были в базе, но не пришли в запросе (по ID)
        # Это эффективно, если db_workout_exercise.sets это InstrumentedList и настроен cascade="all, delete-orphan"
        # В этом случае, простое присвоение новой коллекции удалит старые "осиротевшие" объекты.
        # db_workout_exercise.sets = new_sets_for_workout_exercise

        # Более явный способ удаления, если нет уверенности в каскадах для orphan removal при простом присвоении:
        sets_to_delete = []
        for existing_set_id, existing_set_obj in current_db_sets_map.items():
            if existing_set_id not in input_set_ids_processed:
                sets_to_delete.append(existing_set_obj)
        
        for set_to_del in sets_to_delete:
            await db.delete(set_to_del)
        
        # Обновляем коллекцию. SQLAlchemy отследит изменения.
        # Если new_sets_for_workout_exercise содержит объекты, которые уже были в сессии (обновленные),
        # и новые объекты (еще не добавленные явно в сессию через db.add()),
        # присвоение коллекции должно сработать.
        # Новые объекты, добавленные в коллекцию, будут автоматически добавлены в сессию при flush/commit.
        db_workout_exercise.sets = new_sets_for_workout_exercise


    await db.commit()

    # 4. Получаем обновленный объект со всеми связями для ответа
    # Это гарантирует, что все изменения, включая ID новых сетов, отразятся.
    stmt_final_select = (
        select(WorkoutExercise)
        .options(
            selectinload(WorkoutExercise.sets),
            selectinload(WorkoutExercise.exercise)
            # selectinload(WorkoutExercise.workout) # Если workout нужен в ответе
        )
        .where(WorkoutExercise.id == db_workout_exercise.id)
    )
    result_final = await db.execute(stmt_final_select)
    updated_workout_exercise = result_final.scalar_one_or_none()
    
    if not updated_workout_exercise:
        # Этого не должно произойти, если commit прошел успешно
        raise HTTPException(status_code=500, detail="Не удалось получить обновленное упражнение для тренировки после сохранения")

    return updated_workout_exercise