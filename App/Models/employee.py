from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Float,
    text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    user_companies = relationship("UserCompany", back_populates="company")


class UserCompany(Base):
    __tablename__ = "user_company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    salary = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    # Relationships (optional)
    user = relationship("User", back_populates="user_companies")
    company = relationship("Company", back_populates="user_companies")
