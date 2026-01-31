from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.rbac import Role, Permission
from app.models.user import User
from app.schemas.rbac import RoleCreate, PermissionCreate, RoleUpdate

class RBACService:
    async def get_role_by_name(self, db: AsyncSession, name: str):
        result = await db.execute(select(Role).filter(Role.name == name))
        return result.scalars().first()

    async def create_role(self, db: AsyncSession, role_in: RoleCreate):
        db_role = Role(name=role_in.name, description=role_in.description)
        
        if role_in.permissions:
            # Fetch permissions by name
            result = await db.execute(select(Permission).filter(Permission.name.in_(role_in.permissions)))
            permissions = result.scalars().all()
            db_role.permissions = list(permissions)
            
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        return db_role

    async def create_permission(self, db: AsyncSession, perm_in: PermissionCreate):
        db_perm = Permission(name=perm_in.name, description=perm_in.description)
        db.add(db_perm)
        await db.commit()
        await db.refresh(db_perm)
        return db_perm

    async def assign_role_to_user(self, db: AsyncSession, user_id: int, role_name: str):
        # Fetch user
        user_result = await db.execute(select(User).filter(User.id == user_id).options(selectinload(User.roles)))
        user = user_result.scalars().first()
        if not user:
            return None

        # Fetch role
        role = await self.get_role_by_name(db, role_name)
        if not role:
            return None

        if role not in user.roles:
            user.roles.append(role)
            await db.commit()
            await db.refresh(user)
        return user

    async def get_roles(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Role).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_role_by_id(self, db: AsyncSession, role_id: int):
        result = await db.execute(select(Role).filter(Role.id == role_id))
        return result.scalars().first()

    async def update_role(self, db: AsyncSession, role_id: int, role_in: RoleUpdate):
        role = await self.get_role_by_id(db, role_id)
        if not role:
            return None

        role.name = role_in.name
        if role_in.description is not None:
            role.description = role_in.description
        
        if role_in.permissions is not None:
            # Update permissions
            # Clear existing
            role.permissions.clear()
            if role_in.permissions:
                 result = await db.execute(select(Permission).filter(Permission.name.in_(role_in.permissions)))
                 permissions = result.scalars().all()
                 role.permissions = list(permissions)

        await db.commit()
        await db.refresh(role)
        return role

    async def delete_role(self, db: AsyncSession, role_id: int):
        role = await self.get_role_by_id(db, role_id)
        if not role:
            return False
        await db.delete(role)
        await db.commit()
        return True

    async def remove_role_from_user(self, db: AsyncSession, user_id: int, role_id: int):
        user_result = await db.execute(select(User).filter(User.id == user_id).options(selectinload(User.roles)))
        user = user_result.scalars().first()
        if not user:
            return None
        
        role_to_remove = None
        for role in user.roles:
            if role.id == role_id:
                role_to_remove = role
                break
        
        if role_to_remove:
            user.roles.remove(role_to_remove)
            await db.commit()
            await db.refresh(user)
        
        return user

rbac_service = RBACService()
