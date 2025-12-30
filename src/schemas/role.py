from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.permission import PermissionResponse


class RoleBase(BaseModel):
    """Schema base para Role."""
    name: str = Field(..., min_length=1, max_length=50)


class RoleCreate(RoleBase):
    """Schema para crear un rol."""
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "moderator"
            }
        }
    }


class RoleResponse(RoleBase):
    """Schema para respuesta de rol."""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class RoleWithPermissionsResponse(RoleResponse):
    """Schema para respuesta de rol con sus permisos."""
    permissions: List[PermissionResponse] = []


class RoleListResponse(BaseModel):
    """Schema para respuesta de lista de roles."""
    items: List[RoleWithPermissionsResponse]
    total: int


class AssignPermissionsRequest(BaseModel):
    """Schema para asignar permisos a un rol."""
    permission_names: List[str] = Field(
        ..., 
        min_length=1,
        description="Lista de nombres de permisos a asignar"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "permission_names": ["create_task", "read_task", "update_task"]
            }
        }
    }
