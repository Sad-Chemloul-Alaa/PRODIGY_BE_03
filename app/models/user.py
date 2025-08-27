from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,unique=True,index=True)
    user_name = Column(String(50),nullable=False)
    user_email = Column(String(100),unique=True,nullable=False)
    user_age = Column(Integer(),nullable=False)

    __table_args__ = (
        CheckConstraint('user_age >= 0 AND user_age <= 120', name='check_user_age'),
    )

