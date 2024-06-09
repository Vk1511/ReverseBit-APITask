from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, select
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .base import Base
from app.config.database import AsyncReverseBitDBSessionFactory
from .employee import UserCompany


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    # phone can be more accuratly defined with country code and number of digit
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active_user = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    user_companies = relationship("UserCompany", back_populates="user")

    @classmethod
    async def get_specific_user(
        cls,
        db_session: AsyncReverseBitDBSessionFactory,
        user: String,
        is_email: Boolean = True,
    ):
        if is_email:
            stmt = select(cls).where(cls.email == user)
        else:
            stmt = select(cls).where(cls.id == user)

        result = await db_session.execute(stmt)
        user = result.fetchone()
        # user = result.unique().scalars().all()
        # json_compatible_permission = jsonable_encoder(user)
        return user[0] if len(user) else False

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

    async def update(self, db_session: AsyncReverseBitDBSessionFactory, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        await self.save(db_session)
