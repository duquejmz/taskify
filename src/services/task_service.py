from math import ceil
from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.models.task import Task, TaskStatus, TaskPriority
from src.models.tag import Tag
from src.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Servicio para operaciones con tareas."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, task_data: TaskCreate, user_id: UUID) -> Task:
        """Crea una nueva tarea."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=TaskStatus(task_data.status.value),
            priority=TaskPriority(task_data.priority.value),
            user_id=user_id,
        )
        
        # Agregar tags si se proporcionaron (por nombre)
        if task_data.tag_names:
            tags = self.db.query(Tag).filter(Tag.name.in_(task_data.tag_names)).all()
            task.tags = tags
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Obtiene una tarea por ID (solo si pertenece al usuario)."""
        return self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
    
    def get_tasks_paginated(
        self, 
        user_id: UUID,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Tuple[List[Task], int]:
        """Obtiene tareas paginadas del usuario."""
        query = self.db.query(Task).filter(Task.user_id == user_id)
        
        # Filtros opcionales
        if status:
            query = query.filter(Task.status == TaskStatus(status))
        if priority:
            query = query.filter(Task.priority == TaskPriority(priority))
        
        # Contar total antes de paginar
        total = query.count()
        
        # Ordenar y paginar
        tasks = (
            query
            .order_by(desc(Task.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        
        return tasks, total
    
    def update_task(
        self, 
        task_id: UUID, 
        user_id: UUID, 
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Actualiza una tarea existente."""
        task = self.get_task_by_id(task_id, user_id)
        
        if not task:
            return None
        
        # Actualizar solo campos proporcionados
        update_data = task_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "tag_names" and value is not None:
                tags = self.db.query(Tag).filter(Tag.name.in_(value)).all()
                task.tags = tags
            elif field == "status" and value is not None:
                setattr(task, field, TaskStatus(value))
            elif field == "priority" and value is not None:
                setattr(task, field, TaskPriority(value))
            elif value is not None:
                setattr(task, field, value)
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Elimina una tarea."""
        task = self.get_task_by_id(task_id, user_id)
        
        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    @staticmethod
    def calculate_total_pages(total: int, page_size: int) -> int:
        """Calcula el total de páginas."""
        return ceil(total / page_size) if total > 0 else 1


def get_task_service(db: Session) -> TaskService:
    """Factory para crear TaskService."""
    return TaskService(db)
