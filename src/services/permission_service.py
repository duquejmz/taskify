from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from src.models.permission import Permission
from src.schemas.permission import PermissionCreate


class PermissionService:
    """Servicio para operaciones con permisos."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_permission_by_id(self, permission_id: UUID) -> Optional[Permission]:
        """Obtiene un permiso por ID."""
        return self.db.query(Permission).filter(Permission.id == permission_id).first()
    
    def get_permission_by_name(self, name: str) -> Optional[Permission]:
        """Obtiene un permiso por nombre."""
        return self.db.query(Permission).filter(Permission.name == name).first()
    
    def create_permission(self, permission_data: PermissionCreate) -> Permission:
        """Crea un nuevo permiso."""
        permission = Permission(name=permission_data.name)
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission
    
    def get_all_permissions(self) -> List[Permission]:
        """Obtiene todos los permisos."""
        return self.db.query(Permission).order_by(Permission.name).all()
    
    def get_permissions_by_names(self, names: List[str]) -> List[Permission]:
        """Obtiene permisos por lista de nombres."""
        return self.db.query(Permission).filter(Permission.name.in_(names)).all()


def get_permission_service(db: Session) -> PermissionService:
    """Factory para crear PermissionService."""
    return PermissionService(db)
