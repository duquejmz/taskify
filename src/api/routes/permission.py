from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.deps import AdminUser
from src.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionListResponse,
)
from src.services.permission_service import get_permission_service


router = APIRouter(prefix="/permissions", tags=["Permisos"])


@router.post(
    "",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear permiso",
    description="Crea un nuevo permiso. Solo administradores.",
)
def create_permission(
    permission_data: PermissionCreate,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo permiso (solo admin).
    
    - **name**: Nombre único del permiso (ej: "create_task", "delete_user")
    - **description**: Descripción opcional del permiso
    """
    permission_service = get_permission_service(db)
    
    existing = permission_service.get_permission_by_name(permission_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El permiso '{permission_data.name}' ya existe en el sistema",
        )
    
    permission = permission_service.create_permission(permission_data, admin_user.id)
    return permission


@router.get(
    "",
    response_model=PermissionListResponse,
    summary="Listar permisos",
    description="Obtiene la lista de todos los permisos. Solo administradores.",
)
def list_permissions(
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Lista todos los permisos (solo admin).
    """
    permission_service = get_permission_service(db)
    permissions = permission_service.get_all_permissions()
    
    return PermissionListResponse(
        items=permissions,
        total=len(permissions),
    )
