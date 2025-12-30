from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.models.role import Role
from src.models.user import User
from src.models.permission import Permission
from src.schemas.role import RoleCreate


class RoleService:
    """Servicio para operaciones con roles."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """Obtiene un rol por ID."""
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Obtiene un rol por nombre."""
        return self.db.query(Role).filter(Role.name == name).first()
    
    def create_role(self, role_data: RoleCreate) -> Role:
        """Crea un nuevo rol."""
        role = Role(name=role_data.name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def get_all_roles(self) -> List[Role]:
        """Obtiene todos los roles."""
        return self.db.query(Role).order_by(Role.name).all()
    
    def assign_permissions_to_role(
        self, 
        role_id: UUID, 
        permissions: List[Permission]
    ) -> Optional[Role]:
        """Asigna permisos a un rol."""
        role = self.get_role_by_id(role_id)
        if not role:
            return None
        
        role.permissions = permissions
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def get_users_by_role_name(self, role_name: str) -> Tuple[List[User], int]:
        """Obtiene usuarios por nombre de rol."""
        role = self.get_role_by_name(role_name)
        if not role:
            return [], 0
        
        users = self.db.query(User).filter(User.role_id == role.id).all()
        return users, len(users)
    
    def get_users_by_role(
        self,
        role_id: UUID,
        page: int = 1,
        page_size: int = 10,
        is_active: Optional[bool] = None,
    ) -> Tuple[List[User], int]:
        """Obtiene usuarios por ID de rol con paginación."""
        query = self.db.query(User).filter(User.role_id == role_id)
        
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


def get_role_service(db: Session) -> RoleService:
    """Factory para crear RoleService."""
    return RoleService(db)
