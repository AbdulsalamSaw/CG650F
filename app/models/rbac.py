from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association Table for User <-> Role
role_user = Table(
    "role_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

# Association Table for Role <-> Permission
permission_role = Table(
    "permission_role",
    Base.metadata,
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    guard_name = Column(String(50), default="web")
    description = Column(String(255), nullable=True)

    # Relationships
    permissions = relationship("Permission", secondary=permission_role, back_populates="roles", lazy="selectin")
    users = relationship("User", secondary=role_user, back_populates="roles", lazy="selectin")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False) # e.g., 'edit_posts'
    guard_name = Column(String(50), default="web")
    description = Column(String(255), nullable=True)

    # Relationships
    roles = relationship("Role", secondary=permission_role, back_populates="permissions")
