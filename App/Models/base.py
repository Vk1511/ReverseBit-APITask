from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy import Column, Integer, TIMESTAMP, text
from fastapi import HTTPException, status
from typing import Any
from app.config.database import AsyncReverseBitDBSessionFactory
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


@as_declarative()
class BaseReadOnly:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

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

    async def delete(self, db_session):
        try:
            await db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as sql_error:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(sql_error)
            ) from sql_error
