import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;':"",./<>?]).{8,}$"
)


class LoginRequest(BaseModel):
    """Schema para la solicitud de login. Puede usar email o username."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Valida que la contraseña cumpla con los requisitos de seguridad."""
        if not PASSWORD_REGEX.match(v):
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres, "
                "una mayúscula, una minúscula, un número y un carácter especial"
            )
        return v

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
