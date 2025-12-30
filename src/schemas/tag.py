from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    """Schema base para Tag."""
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    """Schema para crear un tag."""
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "urgente"
            }
        }
    }


class TagResponse(TagBase):
    """Schema para respuesta de tag."""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TagListResponse(BaseModel):
    """Schema para respuesta de lista de tags."""
    items: List[TagResponse]
    total: int
