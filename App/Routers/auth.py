import pytz
from fastapi import APIRouter, Response, Request, Depends, status
from typing import Union
from datetime import datetime
from app.schema.common import GenericDataResponseModel, ErrorResponseModel
from app.schema.auth import UserCreate, UserLogin
from app.config.database import AsyncReverseBitDBSessionFactory, get_reversebit_db
from app.models.auth import User
from app.services.jwt import (
    get_password_hash,
    verify_password,
    create_access_refresh_token,
)
from .constant import REGISTER, LOGIN, UPDATE_USER
from app.exception import ReverseBitException

router = APIRouter(prefix="/auth")


@router.post(
    f"/{REGISTER}", response_model=Union[GenericDataResponseModel, ErrorResponseModel]
)
async def create_user(
    request: Request,
    body: UserCreate,
    response: Response,
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):

    try:
        email = body.email

        # check user already exists
        is_user_exists = await User.get_specific_user(
            db_session=reverse_bit_db_session, user=email
        )
        if is_user_exists:
            raise ReverseBitException(
                message="User already exists with email.",
                status_code=status.HTTP_409_CONFLICT,
            )
        else:
            user_id = await User(
                first_name=body.first_name,
                last_name=body.last_name,
                address=body.address,
                email=email,
                phone=body.phone,
                password=get_password_hash(password=body.password),
            ).save(db_session=reverse_bit_db_session)

        response = GenericDataResponseModel(
            status=True,
            data={
                "first_name": body.first_name,
                "last_name": body.last_name,
                "email": body.email,
            },
            message=f"User with {user_id} user id created successfully.",
            code=status.HTTP_201_CREATED,
            timestamp=str(datetime.now(pytz.utc)),
        )
    except ReverseBitException as e:
        response.status_code = e.status_code
        response = ErrorResponseModel(
            status=False,
            timestamp=str(datetime.now(pytz.utc)),
            data={
                "message": str(e.message),
                "code": e.status_code,
            },
        )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = ErrorResponseModel(
            status=False,
            timestamp=str(datetime.now(pytz.utc)),
            data={
                "message": str(e),
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    return response


# API to authenticate user
"""
    param: UserLogin(email, password)
    response: token (Access token, refresh token)
"""


@router.post(
    f"/{LOGIN}", response_model=Union[GenericDataResponseModel, ErrorResponseModel]
)
async def validate_user(
    request: Request,
    body: UserLogin,
    response: Response,
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):

    try:
        email = body.email
        password = body.password

        # check user already exists
        user_details = await User.get_specific_user(
            db_session=reverse_bit_db_session, user=email
        )
        print("user_details", user_details)
        if not user_details:
            raise ReverseBitException(
                message="User doesn't exist. Please register the user.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        else:
            _ = verify_password(
                plain_password=password,
                hashed_password=user_details.password,
            )
            token = create_access_refresh_token(email=email)

        response = GenericDataResponseModel(
            status=True,
            data=token,
            message=f"User logged-in successfully.",
            code=status.HTTP_201_CREATED,
            timestamp=str(datetime.now(pytz.utc)),
        )
    except ReverseBitException as e:
        response.status_code = e.status_code
        response = ErrorResponseModel(
            status=False,
            timestamp=str(datetime.now(pytz.utc)),
            data={
                "message": str(e.message),
                "code": e.status_code,
            },
        )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = ErrorResponseModel(
            status=False,
            timestamp=str(datetime.now(pytz.utc)),
            data={
                "message": str(e),
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

    return response
