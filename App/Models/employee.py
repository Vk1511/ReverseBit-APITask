from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Float,
    text,
    ForeignKey,
    select,
)
from sqlalchemy.orm import relationship
from app.config.database import AsyncReverseBitDBSessionFactory
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    salary = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    # Relationships (optional)
    user = relationship("User", back_populates="user_companies")
    company = relationship("Company", back_populates="user_companies")

    async def save(self, db_session: AsyncReverseBitDBSessionFactory, flush=None):
        """

        :param db_session:
        :return: Record ID
        """
        try:
            db_session.add(self)
            if not flush:
                await db_session.commit()
            else:
                await db_session.flush()
            return self.id

        except IntegrityError as integrity_error:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Record already exists.",
            )

        except SQLAlchemyError as sql_error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(sql_error)
            ) from sql_error
