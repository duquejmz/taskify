from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.auth import LoginRequest, TokenResponse
from src.services.auth_service import get_auth_service

from src.models.task import Task
from src.models.tag import Tag
from src.models.role import Role
from src.models.permission import Permission


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve un token JWT.",
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Endpoint de login.
    
    - **email**: Email del usuario (opcional si se proporciona username)
    - **username**: Username del usuario (opcional si se proporciona email)
    - **password**: Contraseña del usuario
    
    Retorna un token JWT válido por el tiempo configurado.
    """
    auth_service = get_auth_service(db)
    
    user, error_message = auth_service.authenticate_user(
        email=login_data.email,
        username=login_data.username,
        password=login_data.password,
    )
    
    if not user:
        # Determinar código de error basado en el mensaje
        status_code = status.HTTP_401_UNAUTHORIZED
        if error_message and "desactivada" in error_message:
            status_code = status.HTTP_403_FORBIDDEN
        
        raise HTTPException(
            status_code=status_code,
            detail=error_message or "Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_token_for_user(user)
    
    return TokenResponse(access_token=access_token)
