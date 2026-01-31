from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    db_user = await user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users

# User Role Management
from app.services.rbac_service import rbac_service # Import here to use RBAC service

@router.post("/{user_id}/roles/{role_id}", response_model=UserResponse)
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.edit"))
):
    """
    Assign a role to a user.
    """
    # We need to look up role name by ID because service uses name for assignment logic?
    # Let's check service. assign_role_to_user takes role_name.
    # We should probably update service to take ID, or fetch name here.
    # For efficiency let's fetch role first.
    
    role = await rbac_service.get_role_by_id(db, role_id)
    if not role:
         raise HTTPException(status_code=404, detail="Role not found")
         
    user = await rbac_service.assign_role_to_user(db, user_id, role.name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}/roles/{role_id}", response_model=UserResponse)
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.edit"))
):
    """
    Remove a role from a user.
    """
    user = await rbac_service.remove_role_from_user(db, user_id, role_id)
    if not user:
        raise HTTPException(status_code=404, detail="User or Role not found")
    return user
