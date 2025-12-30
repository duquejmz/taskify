from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator


class LoginRequest(BaseModel):
    """Schema para la solicitud de login. Puede usar email o username."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def validate_identifier(self):
        """Valida que se proporcione email o username."""
        if not self.email and not self.username:
            raise ValueError("Debe proporcionar email o username")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@test.com",
                    "password": "Admin123*"
                },
                {
                    "username": "admin",
                    "password": "Admin123*"
                }
            ]
        }
    }


class TokenResponse(BaseModel):
    """Schema para la respuesta del token."""
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }
