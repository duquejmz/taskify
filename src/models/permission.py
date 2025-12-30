from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.models.mixins import AuditMixin
from src.models.association import permission_role


class Permission(Base, AuditMixin):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, unique=True)

    roles = relationship("Role", secondary=permission_role, back_populates="permissions", lazy="selectin")
