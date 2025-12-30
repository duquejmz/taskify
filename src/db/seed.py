from sqlalchemy.orm import Session

from src.models.user import User
from src.models.role import Role
from src.models.permission import Permission
from src.core.security import hash_password


def seed_initial_data(db: Session) -> None:
    """
    Seed inicial del sistema:
    - Roles
    - Permisos
    - Usuario administrador
    """

    # ---------- PERMISOS ----------
    permissions_data = [
        "create_task",
        "update_task",
        "delete_task",
        "view_task",
        "manage_users",
        "manage_roles",
    ]

    permissions = {}
    for perm_name in permissions_data:
        permission = db.query(Permission).filter_by(name=perm_name).first()
        if not permission:
            permission = Permission(name=perm_name)
            db.add(permission)
        permissions[perm_name] = permission

    db.flush()

    # ---------- ROLES ----------
    roles_data = {
        "admin": permissions_data,
        "user": ["view_task", "create_task"],
    }

    roles = {}
    for role_name, perms in roles_data.items():
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)

        role.permissions = [permissions[p] for p in perms]
        roles[role_name] = role

    db.flush()

    # ---------- USUARIO ADMIN ----------
    admin_email = "admin@test.com"

    admin = db.query(User).filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            name="Administrador",
            username="admin",
            email=admin_email,
            password=hash_password("Admin123*"),
            role_id=roles["admin"].id,
            is_active=True,
        )
        db.add(admin)

    db.commit()
