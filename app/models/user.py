from sqlalchemy import Column, Integer, String, CheckConstraint, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLAlchemyEnum
import uuid
import enum
from app.core.database import Base


class Role(str , enum.Enum):
    admin = "admin"
    normal_user = "user"

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,unique=True,index=True)
    user_name = Column(String(50),nullable=False)
    user_email = Column(String(100),unique=True, nullable=False,  index=True)
    user_age = Column(Integer(),nullable=False)
    user_hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean , default=False)
    user_role = Column(SQLAlchemyEnum(Role) , default=Role.normal_user , nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    __table_args__ = (
        CheckConstraint('user_age >= 0 AND user_age <= 120', name='check_user_age'),
    )

