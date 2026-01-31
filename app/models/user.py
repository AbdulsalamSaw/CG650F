from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # RBAC Relationship
    from app.models.rbac import role_user # Late import to avoid circular dependency
    from sqlalchemy.orm import relationship
    roles = relationship("Role", secondary="role_user", back_populates="users", lazy="selectin")
