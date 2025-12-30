from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.user import User
from src.core.security import verify_access_token


class CustomHTTPBearer(HTTPBearer):
    """HTTPBearer personalizado con mensajes en español."""
    
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        try:
            credentials = await super().__call__(request)
            return credentials
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se proporcionó token de autenticación. Incluya el header 'Authorization: Bearer <token>'",
                headers={"WWW-Authenticate": "Bearer"},
            )


security = CustomHTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db),
) -> User:
    """Dependencia para obtener el usuario actual desde el token JWT."""
    token = credentials.credentials
    
    user_id = verify_access_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == UUID(user_id)).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependencia para verificar que el usuario tiene rol admin."""
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción. Se requiere rol de administrador.",
        )
    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(get_admin_user)]
