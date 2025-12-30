from uuid import uuid4
from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.models.mixins import AuditMixin
from src.models.association import task_tag


class Tag(Base, AuditMixin):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)

    tasks = relationship("Task", secondary=task_tag, back_populates="tags", lazy="selectin")

    __table_args__ = (
        Index("ix_tags_name", "name"),
        Index("ix_tags_created_at", "created_at"),
    )
