from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Index,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.models.mixins import AuditMixin
from src.core.security import hash_password, verify_password


class User(Base, AuditMixin):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    name = Column(
        String(150),
        nullable=False
    )

    username = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    role = relationship(
        "Role",
        back_populates="users"
    )

    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Genera y guarda el hash de la contraseña."""
        self.password_hash = hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado."""
        return verify_password(password, self.password_hash)

    def deactivate(self) -> None:
        """Desactiva el usuario sin borrarlo."""
        self.is_active = False


Index("idx_user_username_email", User.username, User.email)
