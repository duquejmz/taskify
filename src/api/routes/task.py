from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.deps import CurrentUser
from src.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)
from src.services.task_service import get_task_service


router = APIRouter(prefix="/tasks", tags=["Tareas"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tarea",
    description="Crea una nueva tarea para el usuario autenticado.",
)
def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """
    Crea una nueva tarea.
    
    - **title**: Título de la tarea (requerido)
    - **description**: Descripción de la tarea (opcional)
    - **status**: Estado de la tarea (pending, in_progress, completed)
    - **priority**: Prioridad de la tarea (low, medium, high)
    - **tag_ids**: Lista de IDs de tags (opcional)
    """
    task_service = get_task_service(db)
    task = task_service.create_task(task_data, current_user.id)
    return task


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Listar tareas",
    description="Obtiene las tareas del usuario autenticado con paginación.",
)
def list_tasks(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridad"),
):
    """
    Lista las tareas del usuario con paginación.
    
    - **page**: Número de página (default: 1)
    - **page_size**: Cantidad de items por página (default: 10, max: 100)
    - **status**: Filtrar por estado (pending, in_progress, completed)
    - **priority**: Filtrar por prioridad (low, medium, high)
    """
    task_service = get_task_service(db)
    
    tasks, total = task_service.get_tasks_paginated(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        status=status,
        priority=priority,
    )
    
    total_pages = task_service.calculate_total_pages(total, page_size)
    
    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Obtener tarea",
    description="Obtiene una tarea específica por su ID.",
)
def get_task(
    task_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Obtiene una tarea por su ID."""
    task_service = get_task_service(db)
    task = task_service.get_task_by_id(task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Actualizar tarea",
    description="Actualiza una tarea existente.",
)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """
    Actualiza una tarea existente.
    
    Solo se actualizan los campos proporcionados.
    """
    task_service = get_task_service(db)
    task = task_service.update_task(task_id, current_user.id, task_data)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tarea",
    description="Elimina una tarea existente.",
)
def delete_task(
    task_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Elimina una tarea por su ID."""
    task_service = get_task_service(db)
    deleted = task_service.delete_task(task_id, current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada",
        )
    
    return None
