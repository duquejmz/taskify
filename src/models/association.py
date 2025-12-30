from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

task_tag = Table(
    "task_tag",
    Base.metadata,
    Column("task_id", ForeignKey("task.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)

permissions_role = Table(
    "permissions_role",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)
