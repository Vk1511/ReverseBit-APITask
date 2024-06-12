from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    select,
)
from sqlalchemy.orm import relationship
from app.config.database import AsyncReverseBitDBSessionFactory
from .base import Base


class Company(Base):
    __tablename__ = "companies"

    company_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=False)

    user_companies = relationship("UserCompany", back_populates="company")

    @classmethod
    async def get_specific_company(
        cls,
        db_session: AsyncReverseBitDBSessionFactory,
        company: String,
    ):
        stmt = select(cls).where(cls.id == company)

        result = await db_session.execute(stmt)
        user = result.fetchone()
        return user[0] if user else False


class UserCompany(Base):
    __tablename__ = "user_company"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    salary = Column(Float, nullable=False)

    # Relationships (optional)
    user = relationship("User", back_populates="user_companies")
    company = relationship("Company", back_populates="user_companies")
