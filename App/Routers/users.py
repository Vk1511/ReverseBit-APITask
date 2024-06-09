import pytz
from fastapi import APIRouter, Response, Request, Depends, status, Query
from typing import Union
from datetime import datetime
from app.schema.common import GenericDataResponseModel, ErrorResponseModel
from app.schema.auth import UserUpdate, UserResponse
from app.schema.employee import AddUserComapny
from app.config.database import AsyncReverseBitDBSessionFactory, get_reversebit_db
from app.models.auth import User
from app.models.employee import Company, UserCompany
from app.services.jwt import (
    get_current_user,
)
from app.exception import ReverseBitException
from .constant import UPDATE_USER, COMPANY

router = APIRouter(prefix=f"/{UPDATE_USER}")


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
            message=f"User details updated successfully.",
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
            message=f"User details updated successfully.",
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


@router.delete(
    "/{user_id}",
    response_model=Union[GenericDataResponseModel, ErrorResponseModel],
)
async def delete_user(
    request: Request,
    user_id: int,
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
            _ = await user_details.delete(db_session=reverse_bit_db_session)

        response = GenericDataResponseModel(
            status=True,
            data={},
            message=f"User with {user_id} deleted successfully.",
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


@router.get(
    "/{user_id}",
    response_model=Union[GenericDataResponseModel, ErrorResponseModel],
)
async def fetch_user(
    request: Request,
    user_id: int,
    response: Response,
    user: str = Depends(get_current_user),
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):
    try:
        # check user already exists
        user_details = await User.get_specific_user_details_with_company_data(
            db_session=reverse_bit_db_session, user=user_id
        )
        if not user_details:
            raise ReverseBitException(
                message="For given user id, user doesn't exist. ",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        response = GenericDataResponseModel(
            status=True,
            data=UserResponse.from_orm(user_details).dict(),
            message=f"User details fetched successfully.",
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


@router.get(
    "",
    response_model=Union[GenericDataResponseModel, ErrorResponseModel],
)
async def fetch_users(
    request: Request,
    response: Response,
    is_higher_salary: bool = Query(
        False, description="Whether to filter users by higher salary"
    ),
    user: str = Depends(get_current_user),
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):
    try:
        # check user already exists
        user_details = await User.get_users_details_with_company_data(
            db_session=reverse_bit_db_session, is_higher_salary=is_higher_salary
        )
        user_data = [UserResponse.from_orm(user).dict() for user in user_details]

        response = GenericDataResponseModel(
            status=True,
            data=user_data,
            message=f"User details fetched successfully.",
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


@router.post(
    f"/{COMPANY}" + "/{user_id}",
    response_model=Union[GenericDataResponseModel, ErrorResponseModel],
)
async def create_user(
    request: Request,
    body: AddUserComapny,
    user_id: int,
    response: Response,
    reverse_bit_db_session: AsyncReverseBitDBSessionFactory = Depends(
        get_reversebit_db
    ),
):

    try:
        # check user already exists
        is_user_exists = await User.get_specific_user(
            db_session=reverse_bit_db_session, user=user_id, is_email=False
        )
        if not is_user_exists:
            raise ReverseBitException(
                message="User not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        else:
            is_company_exists = await Company.get_specific_company(
                db_session=reverse_bit_db_session, company=body.company_id
            )
            if not is_company_exists:
                raise ReverseBitException(
                    message="Invalid company is passed",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            else:
                user_id = await UserCompany(
                    user_id=user_id, company_id=body.company_id, salary=body.salary
                ).save(db_session=reverse_bit_db_session)

        response = GenericDataResponseModel(
            status=True,
            data=body.dict(),
            message=f"Company data added for user id {user_id} successfully.",
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
