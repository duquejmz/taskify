from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Schema base para User."""
    name: str = Field(..., min_length=1, max_length=150)
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """Schema para crear un usuario."""
    password: str = Field(..., min_length=8, max_length=100)
    role_name: Optional[str] = Field(default="user", description="Nombre del rol (por defecto: user)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Juan Pérez",
                    "username": "juanperez",
                    "email": "juan@example.com",
                    "password": "Password123*"
                },
                {
                    "name": "Admin User",
                    "username": "adminuser",
                    "email": "admin2@example.com",
                    "password": "Password123*",
                    "role_name": "admin"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class RoleInfo(BaseModel):
    """Schema simplificado para mostrar info del rol."""
    id: UUID
    name: str

    model_config = {"from_attributes": True}


class UserResponse(UserBase):
    """Schema para respuesta de usuario."""
    id: UUID
    is_active: bool
    role: RoleInfo
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Schema para respuesta paginada de usuarios."""
    items: List[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class UserInDB(UserResponse):
    """Schema de usuario con datos de BD."""
    password: str
