from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.models.user import User
from src.core.security import verify_password, create_access_token


class AuthService:
    """Servicio de autenticación."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(
        self, 
        password: str,
        email: Optional[str] = None, 
        username: Optional[str] = None,
    ) -> Optional[User]:
        """Autentica un usuario por email o username y contraseña."""
        if email:
            user = self.db.query(User).filter(User.email == email).first()
        elif username:
            user = self.db.query(User).filter(User.username == username).first()
        else:
            return None
        
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not verify_password(password, user.password):
            return None
        
        return user
    
    def create_token_for_user(self, user: User) -> str:
        """Crea un token de acceso para el usuario."""
        return create_access_token(user_id=user.id)
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        return self.db.query(User).filter(User.id == user_id).first()


def get_auth_service(db: Session) -> AuthService:
    """Factory para crear AuthService."""
    return AuthService(db)
