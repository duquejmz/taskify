from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.deps import CurrentUser, AdminUser
from src.schemas.tag import TagCreate, TagResponse, TagListResponse
from src.schemas.task import TaskResponse
from src.services.tag_service import get_tag_service

# Importar modelos para resolver relaciones
from src.models.task import Task
from src.models.role import Role
from src.models.permission import Permission


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear tag",
    description="Crea un nuevo tag. Solo administradores.",
)
def create_tag(
    tag_data: TagCreate,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo tag (solo admin).
    
    - **name**: Nombre único del tag
    """
    tag_service = get_tag_service(db)
    
    # Verificar que el tag no existe
    if tag_service.get_tag_by_name(tag_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tag ya existe",
        )
    
    tag = tag_service.create_tag(tag_data)
    return tag


@router.get(
    "",
    response_model=TagListResponse,
    summary="Listar tags",
    description="Obtiene todos los tags disponibles.",
)
def list_tags(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """Lista todos los tags."""
    tag_service = get_tag_service(db)
    tags, total = tag_service.get_all_tags()
    
    return TagListResponse(items=tags, total=total)


@router.get(
    "/{tag_name}/tasks",
    response_model=list[TaskResponse],
    summary="Obtener tareas por tag",
    description="Obtiene las tareas del usuario que tienen un tag específico.",
)
def get_tasks_by_tag(
    tag_name: str,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """
    Obtiene las tareas del usuario autenticado que tienen el tag especificado.
    """
    tag_service = get_tag_service(db)
    
    # Verificar que el tag existe
    if not tag_service.get_tag_by_name(tag_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El tag '{tag_name}' no existe",
        )
    
    tasks, _ = tag_service.get_tasks_by_tag_name(tag_name, current_user.id)
    return tasks
