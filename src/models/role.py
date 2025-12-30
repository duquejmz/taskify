from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.models.mixins import AuditMixin
from src.models.association import permission_role


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)

    permissions = relationship("Permission", secondary=permission_role, back_populates="roles", lazy="selectin")
    users = relationship("User", back_populates="role", lazy="selectin")
