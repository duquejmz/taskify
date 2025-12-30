from sqlalchemy import Table, Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID

from src.db.base import Base

permission_role = Table(
    "permission_role",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    Index("idx_permission_role_role_id", "role_id"),
    Index("idx_permission_role_permission_id", "permission_id"),
)

task_tag = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Index("idx_task_tag_task_id", "task_id"),
    Index("idx_task_tag_tag_id", "tag_id"),
)

