from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func


class AuditMixin:
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    created_by = Column(
        String(100),
        nullable=True,
        index=True,
    )

    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        nullable=True,
    )

    updated_by = Column(
        String(100),
        nullable=True,
    )
