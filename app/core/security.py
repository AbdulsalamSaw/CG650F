from fastapi import Depends, HTTPException, status
from typing import List
from app.api.v1.endpoints.users import get_db, user_service # Reusing existing dependencies
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

async def get_current_user(db: AsyncSession = Depends(get_db)):
    # In a real app, this would verify a JWT token
    # For now, we'll mock it by getting the first user in the DB
    # or you can implement a proper login flow.
    # We are getting the first user and eagerly loading roles and permissions
    
    # Note: To optimize, we should eager load deeply: User -> Roles -> Permissions
    # Implementation depends on how complex we want this mock to be.
    # For now, let's just fetch user with ID 1
    
    # We need to load roles and permissions too
    stmt = user_service.get_users(db, limit=1) # This doesn't join usually
    
    # Let's do a custom query for current user mocking
    from sqlalchemy.future import select
    from app.models.user import User
    
    # Mocking user ID 1 is logged in
    result = await db.execute(select(User).filter(User.id == 1).options(selectinload(User.roles).selectinload(Role.permissions)))
    user = result.scalars().first()
    
    if not user:
        # If no user exists, maybe throw 401, but for initial setup lets return None or raise
        # raise HTTPException(status_code=401, detail="No mock user found")
        return None 
    return user

from app.models.rbac import Role

def has_permission(perm_name: str):
    async def dependency(user: User = Depends(get_current_user)):
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        
        # Check if user is superuser
        if user.is_superuser:
            return True

        # Check permissions in roles
        has_perm = False
        for role in user.roles:
            for perm in role.permissions:
                if perm.name == perm_name:
                    has_perm = True
                    break
            if has_perm:
                break
        
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User doesn't have required permission: {perm_name}",
            )
        return True
    return dependency

def has_role(role_name: str):
    async def dependency(user: User = Depends(get_current_user)):
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        
        if user.is_superuser:
            return True

        role_names = [role.name for role in user.roles]
        if role_name not in role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User doesn't have required role: {role_name}",
            )
        return True
    return dependency
