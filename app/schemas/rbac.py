from pydantic import BaseModel
from typing import List, Optional

# Permission Schemas
class PermissionBase(BaseModel):
    name: str # e.g. "users.create"
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        from_attributes = True

# Role Schemas
class RoleBase(BaseModel):
    name: str # e.g. "admin"
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permissions: List[str] = [] # List of permission names to assign

class RoleUpdate(RoleBase):
    permissions: Optional[List[str]] = None # List of permission names to update (optional)

class RoleResponse(RoleBase):
    id: int
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True
