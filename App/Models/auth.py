from sqlalchemy import Column, String, Boolean, select, func
from sqlalchemy.orm import relationship, joinedload
from .base import Base
from app.config.database import AsyncReverseBitDBSessionFactory
from .employee import UserCompany


class User(Base):
    __tablename__ = "users"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    # phone can be more accuratly defined with country code and number of digit
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active_user = Column(Boolean, nullable=False, default=True)

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
        return user[0] if user else False

    @classmethod
    async def get_specific_user_details_with_company_data(
        cls,
        db_session: AsyncReverseBitDBSessionFactory,
        user: String,
    ):

        stmt = (
            select(cls)
            .options(joinedload(cls.user_companies).joinedload(UserCompany.company))
            .where(cls.id == user)
        )
        result = await db_session.execute(stmt)
        user = result.scalars().first()

        return user

    @classmethod
    async def get_users_details_with_company_data(
        cls, db_session: AsyncReverseBitDBSessionFactory, is_higher_salary: bool = False
    ):
        stmt = select(cls).options(
            joinedload(cls.user_companies).joinedload(UserCompany.company)
        )

        if is_higher_salary:
            # subquery = (
            #     select(
            #         UserCompany.user_id,
            #         func.max(UserCompany.salary).label("max_salary"),
            #     )
            #     .group_by(UserCompany.user_id)
            #     .having(func.max(UserCompany.salary) > 50000)
            #     .alias("subq")
            # )
            # stmt = stmt.join(subquery, User.id == subquery.c.user_id)
            stmt = (
                select(cls)
                .join(UserCompany)
                .group_by(cls.id)
                .having(func.max(UserCompany.salary) > 50000)
                .options(joinedload(cls.user_companies).joinedload(UserCompany.company))
            )

        result = await db_session.execute(stmt)
        users = result.unique().scalars().all()
        return users
