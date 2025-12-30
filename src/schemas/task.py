from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Estados posibles de una tarea."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Prioridades posibles de una tarea."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    """Schema base para Task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    """Schema para crear una tarea."""
    tag_names: Optional[List[str]] = Field(default=None, description="Lista de nombres de tags")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Implementar autenticación",
                "description": "Agregar JWT al proyecto",
                "status": "pending",
                "priority": "high",
                "tag_names": ["backend", "urgente"]
            }
        }
    }


class TaskUpdate(BaseModel):
    """Schema para actualizar una tarea."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    tag_names: Optional[List[str]] = Field(default=None, description="Lista de nombres de tags")


class TaskResponse(TaskBase):
    """Schema para respuesta de tarea."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    """Schema para respuesta paginada de tareas."""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
