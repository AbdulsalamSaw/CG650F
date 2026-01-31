from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import has_permission
from app.schemas.rbac import RoleCreate, RoleUpdate, RoleResponse
from app.services.rbac_service import rbac_service

router = APIRouter()

@router.get("/", response_model=List[RoleResponse])
async def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.view")) # Example permission
):
    """
    Retrieve roles.
    """
    return await rbac_service.get_roles(db, skip=skip, limit=limit)

@router.post("/", response_model=RoleResponse)
async def create_role(
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.edit"))
):
    """
    Create new role.
    """
    role = await rbac_service.get_role_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system.",
        )
    return await rbac_service.create_role(db=db, role_in=role_in)

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.view"))
):
    """
    Get role by ID.
    """
    role = await rbac_service.get_role_by_id(db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.edit"))
):
    """
    Update a role.
    """
    role = await rbac_service.update_role(db, role_id=role_id, role_in=role_in)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/{role_id}", response_model=Any)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    # authorized: bool = Depends(has_permission("users.delete"))
):
    """
    Delete a role.
    """
    success = await rbac_service.delete_role(db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}
