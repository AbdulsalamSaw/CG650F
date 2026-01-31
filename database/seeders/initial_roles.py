from app.core.database import SessionLocal
from app.services.rbac_service import rbac_service
from app.schemas.rbac import RoleCreate, PermissionCreate
from app.models.rbac import Role, Permission
from sqlalchemy.future import select

async def run():
    async with SessionLocal() as db:
        print("   -> Seeding Permissions & Roles...")
        
        # Permissions
        p_view_users = await rbac_service.create_permission(db, PermissionCreate(name="users.view", description="View users"))
        p_edit_users = await rbac_service.create_permission(db, PermissionCreate(name="users.edit", description="Edit users"))
        p_delete_users = await rbac_service.create_permission(db, PermissionCreate(name="users.delete", description="Delete users"))
        
        # Roles
        admin_role = await rbac_service.create_role(db, RoleCreate(name="admin", description="Administrator", permissions=["users.view", "users.edit", "users.delete"]))
        
        # Manual link in case creation didn't Link (just for safety in seeder)
        admin = (await db.execute(select(Role).filter(Role.name == "admin"))).scalars().first()
        permissions = [p_view_users, p_edit_users, p_delete_users]
        for p in permissions:
            if p not in admin.permissions:
                admin.permissions.append(p)
        
        await db.commit()
        print("   -> Seeding Complete!")
