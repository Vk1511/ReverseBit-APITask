from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, FLOAT, text


class Post(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, required=True, max_length=32)
    last_name = Column(String, nullable=False, max_length=32)
    address = Column(String, nullable=True)
    phone = Column(Integer, nullable=False, max_digits=10)
    salary = Column(FLOAT, nullable=False, max_digits=10, decimal_places=2)
    is_active_user = Column(Boolean, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True))
