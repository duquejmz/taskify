from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from src.models.tag import Tag
from src.models.task import Task
from src.schemas.tag import TagCreate


class TagService:
    """Servicio para operaciones con tags."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_tag_by_id(self, tag_id: UUID) -> Optional[Tag]:
        """Obtiene un tag por ID."""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()
    
    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Obtiene un tag por nombre."""
        return self.db.query(Tag).filter(Tag.name == name).first()
    
    def create_tag(self, tag_data: TagCreate, created_by: UUID) -> Tag:
        """Crea un nuevo tag."""
        tag = Tag(name=tag_data.name, created_by=str(created_by))
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def get_all_tags(self) -> Tuple[List[Tag], int]:
        """Obtiene todos los tags."""
        tags = self.db.query(Tag).order_by(Tag.name).all()
        return tags, len(tags)
    
    def get_tasks_by_tag_name(
        self, 
        tag_name: str, 
        user_id: UUID
    ) -> Tuple[List[Task], int]:
        """Obtiene tareas que tienen un tag específico (solo del usuario)."""
        tag = self.get_tag_by_name(tag_name)
        if not tag:
            return [], 0
        
        tasks = [task for task in tag.tasks if task.user_id == user_id]
        return tasks, len(tasks)


def get_tag_service(db: Session) -> TagService:
    """Factory para crear TagService."""
    return TagService(db)
