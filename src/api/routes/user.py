from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.deps import AdminUser
from src.schemas.user import (
    UserCreate,
    UserResponse,
    UserListResponse,
)
from src.services.user_service import get_user_service


router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario. Solo administradores pueden crear usuarios.",
)
def create_user(
    user_data: UserCreate,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo usuario (solo admin).
    
    - **name**: Nombre completo del usuario
    - **username**: Nombre de usuario único
    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres)
    - **role_name**: Nombre del rol (opcional, por defecto: "user")
    """
    user_service = get_user_service(db)
    
    # Verificar que el email no existe
    if user_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )
    
    # Verificar que el username no existe
    if user_service.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado",
        )
    
    # Buscar el rol por nombre
    role = user_service.get_role_by_name(user_data.role_name)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El rol '{user_data.role_name}' no existe",
        )
    
    user = user_service.create_user(user_data, role.id)
    return user


@router.get(
    "",
    response_model=UserListResponse,
    summary="Listar usuarios",
    description="Obtiene la lista de usuarios con paginación. Solo administradores.",
)
def list_users(
    admin_user: AdminUser,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    is_active: Optional[bool] = Query(True, description="Filtrar por estado activo (default: True, solo activos)"),
):
    """
    Lista usuarios con paginación (solo admin).
    
    - **page**: Número de página (default: 1)
    - **page_size**: Cantidad de items por página (default: 10, max: 100)
    - **is_active**: Filtrar por estado activo/inactivo (default: True)
    """
    user_service = get_user_service(db)
    
    users, total = user_service.get_users_paginated(
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


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
    summary="Desactivar usuario",
    description="Desactiva un usuario (soft delete). Solo administradores.",
)
def deactivate_user(
    user_id: UUID,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Desactiva un usuario (solo admin).
    
    El usuario no será eliminado, solo marcado como inactivo.
    """
    user_service = get_user_service(db)
    
    # No permitir desactivarse a sí mismo
    if admin_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivarte a ti mismo",
        )
    
    user = user_service.deactivate_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    return user


@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
    summary="Reactivar usuario",
    description="Reactiva un usuario previamente desactivado. Solo administradores.",
)
def activate_user(
    user_id: UUID,
    admin_user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Reactiva un usuario (solo admin).
    """
    user_service = get_user_service(db)
    
    user = user_service.activate_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    
    return user
