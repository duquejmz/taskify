from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    """Schema base para Permission."""
    name: str = Field(..., min_length=1, max_length=100)


class PermissionCreate(PermissionBase):
    """Schema para crear un permiso."""
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "delete_users"
            }
        }
    }


class PermissionResponse(PermissionBase):
    """Schema para respuesta de permiso."""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PermissionListResponse(BaseModel):
    """Schema para respuesta de lista de permisos."""
    items: List[PermissionResponse]
    total: int


class AssignPermissionsRequest(BaseModel):
    """Schema para asignar permisos a un rol."""
    permission_names: List[str] = Field(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "permission_names": ["create_task", "view_task", "update_task"]
            }
        }
    }
