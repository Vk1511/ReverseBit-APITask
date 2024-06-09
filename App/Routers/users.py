import pytz
from fastapi import APIRouter, Response, Request, Depends, status
from typing import Union
from datetime import datetime
from app.schema.common import GenericDataResponseModel, ErrorResponseModel
from app.schema.user import UserUpdate
from app.config.database import AsyncReverseBitDBSessionFactory, get_reversebit_db
from app.models.auth import User
from app.services.jwt import (
    get_password_hash,
    verify_password,
    create_access_refresh_token,
    get_current_user,
)
from .constant import REGISTER, LOGIN, UPDATE_USER
from app.exception import ReverseBitException

router = APIRouter(prefix="/user")


@router.put(
    "/{user_id}",
    response_model=Union[GenericDataResponseModel, ErrorResponseModel],
)
async def update_user(
    request: Request,
    user_id: int,
    body: UserUpdate,
    response: Response,
    user: str = Depends(get_current_user),
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):

    try:
        # check user already exists
        user_details = await User.get_specific_user(
            db_session=reverse_bit_db_session, user=user_id, is_email=False
        )
        if not user_details:
            raise ReverseBitException(
                message="For given user id, user doesn't exist. ",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        else:
            try:
                values_need_be_update = body.dict()
                values_need_be_update["updated_at"] = datetime.now(pytz.utc)
                _ = await user_details.update(
                    db_session=reverse_bit_db_session,
                    **values_need_be_update,
                )
            except Exception as e:
                raise ReverseBitException(
                    message="You might, forgot to pass value for not nullable filed like first_name, phone",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        response = GenericDataResponseModel(
            status=True,
            data=body.dict(),
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


@router.patch(
    "/{user_id}",
    response_model=Union[GenericDataResponseModel, ErrorResponseModel],
)
async def partial_update_user(
    request: Request,
    user_id: int,
    body: UserUpdate,
    response: Response,
    user: str = Depends(get_current_user),
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):

    try:
        # check user already exists
        user_details = await User.get_specific_user(
            db_session=reverse_bit_db_session, user=user_id, is_email=False
        )
        if not user_details:
            raise ReverseBitException(
                message="For given user id, user doesn't exist. ",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        else:
            values_need_be_update = body.dict(exclude_unset=True)
            values_need_be_update["updated_at"] = datetime.now(pytz.utc)
            _ = await user_details.update(
                db_session=reverse_bit_db_session,
                **values_need_be_update,
            )

        response = GenericDataResponseModel(
            status=True,
            data=values_need_be_update,
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
