from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.deps import AdminUser
from src.schemas.role import (
    RoleCreate,
    RoleResponse,
    RoleWithPermissionsResponse,
    RoleListResponse,
    UpdatePermissionsRequest,
)
from src.schemas.user import UserListResponse
from src.services.role_service import get_role_service
from src.services.permission_service import get_permission_service
from src.services.user_service import get_user_service


router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear rol",
    description="Crea un nuevo rol. Solo administradores.",
)
def create_role(
    role_data: RoleCreate,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo rol (solo admin).
    
    - **name**: Nombre único del rol (ej: "moderator", "editor")
    - **description**: Descripción opcional del rol
    """
    role_service = get_role_service(db)
    
    # Verificar si ya existe
    existing = role_service.get_role_by_name(role_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El rol '{role_data.name}' ya existe en el sistema",
        )
    
    role = role_service.create_role(role_data, admin_user.id)
    return role


@router.get(
    "",
    response_model=RoleListResponse,
    summary="Listar roles",
    description="Obtiene la lista de todos los roles. Solo administradores.",
)
def list_roles(
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Lista todos los roles (solo admin).
    """
    role_service = get_role_service(db)
    roles = role_service.get_all_roles()
    
    return RoleListResponse(
        items=roles,
        total=len(roles),
    )


@router.get(
    "/{role_id}",
    response_model=RoleWithPermissionsResponse,
    summary="Obtener rol con permisos",
    description="Obtiene un rol con sus permisos asignados. Solo administradores.",
)
def get_role_with_permissions(
    role_id: UUID,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Obtiene un rol con sus permisos (solo admin).
    """
    role_service = get_role_service(db)
    role = role_service.get_role_by_id(role_id)
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado",
        )
    
    return role


@router.patch(
    "/{role_id}/permissions",
    response_model=RoleWithPermissionsResponse,
    summary="Actualizar permisos de rol",
    description="Agrega o quita permisos de un rol. Solo administradores.",
)
def update_role_permissions(
    role_id: UUID,
    permissions_data: UpdatePermissionsRequest,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Actualiza los permisos de un rol (solo admin).
    
    - **add**: Lista de nombres de permisos a agregar
    - **remove**: Lista de nombres de permisos a quitar
    
    Se pueden enviar ambos campos o solo uno de ellos.
    """
    role_service = get_role_service(db)
    permission_service = get_permission_service(db)
    
    # Validar que al menos se proporcione una acción
    if not permissions_data.add and not permissions_data.remove:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe proporcionar al menos permisos para agregar o quitar",
        )
    
    # Verificar que el rol existe
    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado",
        )
    
    # Obtener permisos actuales del rol
    current_permission_names = {p.name for p in role.permissions}
    
    # Validar permisos a agregar
    if permissions_data.add:
        permissions_to_add = permission_service.get_permissions_by_names(permissions_data.add)
        found_add_names = {p.name for p in permissions_to_add}
        missing_add = set(permissions_data.add) - found_add_names
        if missing_add:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Los siguientes permisos no existen: {', '.join(sorted(missing_add))}",
            )
    
    # Validar permisos a quitar
    if permissions_data.remove:
        permissions_to_remove = permission_service.get_permissions_by_names(permissions_data.remove)
        found_remove_names = {p.name for p in permissions_to_remove}
        missing_remove = set(permissions_data.remove) - found_remove_names
        if missing_remove:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Los siguientes permisos no existen: {', '.join(sorted(missing_remove))}",
            )
        
        # Verificar que los permisos a quitar están asignados al rol
        not_assigned = set(permissions_data.remove) - current_permission_names
        if not_assigned:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Los siguientes permisos no están asignados al rol: {', '.join(sorted(not_assigned))}",
            )
    
    # Calcular nuevos permisos
    new_permission_names = current_permission_names.copy()
    new_permission_names.update(permissions_data.add)
    new_permission_names -= set(permissions_data.remove)
    
    # Obtener objetos de permisos finales
    final_permissions = permission_service.get_permissions_by_names(list(new_permission_names))
    
    # Actualizar permisos
    updated_role = role_service.assign_permissions_to_role(role_id, final_permissions, admin_user.id)
    return updated_role


@router.get(
    "/{role_name}/users",
    response_model=UserListResponse,
    summary="Obtener usuarios por rol",
    description="Obtiene los usuarios que tienen un rol específico. Solo administradores.",
)
def get_users_by_role(
    role_name: str,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    is_active: Optional[bool] = Query(True, description="Filtrar por estado activo (default: True, solo activos)"),
):
    """
    Obtiene usuarios por nombre de rol (solo admin).
    
    - **role_name**: Nombre del rol (ej: "admin", "user")
    - **page**: Número de página
    - **page_size**: Cantidad de items por página
    - **is_active**: Filtrar por estado activo/inactivo (default: True)
    """
    role_service = get_role_service(db)
    user_service = get_user_service(db)
    
    # Verificar que el rol existe
    role = role_service.get_role_by_name(role_name)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El rol '{role_name}' no existe",
        )
    
    users, total = role_service.get_users_by_role(
        role_id=role.id,
        page=page,
        page_size=page_size,
        is_active=is_active,
    )
    
    total_pages = user_service.calculate_total_pages(total, page_size)
    
    return UserListResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
