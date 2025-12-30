from math import ceil
from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.models.user import User
from src.models.role import Role
from src.schemas.user import UserCreate, UserUpdate
from src.core.security import hash_password


class UserService:
    """Servicio para operaciones con usuarios."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Obtiene un usuario por ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def check_role_exists(self, role_id: UUID) -> bool:
        """Verifica si un rol existe."""
        return self.db.query(Role).filter(Role.id == role_id).first() is not None
    
    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        """Obtiene un rol por su nombre."""
        return self.db.query(Role).filter(Role.name == role_name).first()
    
    def create_user(self, user_data: UserCreate, role_id: UUID, created_by: UUID) -> User:
        """Crea un nuevo usuario."""
        user = User(
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password),
            role_id=role_id,
            is_active=True,
            created_by=str(created_by),
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_users_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        is_active: Optional[bool] = None,
    ) -> Tuple[List[User], int]:
        """Obtiene usuarios paginados."""
        query = self.db.query(User)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        total = query.count()

        users = (
            query
            .order_by(desc(User.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        
        return users, total
    
    def update_user(self, user_id: UUID, user_data: UserUpdate, updated_by: UUID) -> Optional[User]:
        """Actualiza un usuario existente."""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)
        
        user.updated_by = str(updated_by)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def deactivate_user(self, user_id: UUID, updated_by: UUID) -> Optional[User]:
        """Desactiva un usuario (soft delete)."""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None
        
        user.is_active = False
        user.updated_by = str(updated_by)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def activate_user(self, user_id: UUID, updated_by: UUID) -> Optional[User]:
        """Reactiva un usuario."""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None
        
        user.is_active = True
        user.updated_by = str(updated_by)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    @staticmethod
    def calculate_total_pages(total: int, page_size: int) -> int:
        """Calcula el total de páginas."""
        return ceil(total / page_size) if total > 0 else 1


def get_user_service(db: Session) -> UserService:
    """Factory para crear UserService."""
    return UserService(db)
