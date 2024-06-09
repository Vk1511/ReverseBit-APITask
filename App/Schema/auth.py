from pydantic import BaseModel, Extra, constr
from typing import Optional, List
from .employee import UserCompanyResponse
from datetime import datetime


class UserCreate(BaseModel):
    first_name: constr(min_length=1)
    last_name: str = None
    address: str = None
    phone: constr(min_length=10)
    # TODO: use pydantic[email] instead of str
    email: str
    password: str

    class Config:
        extra = Extra.forbid


class UserLogin(BaseModel):
    email: constr(min_length=1)
    password: constr(min_length=1)

    class Config:
        extra = Extra.forbid


class UserUpdate(BaseModel):
    first_name: Optional[constr(min_length=1)] = None
    last_name: Optional[constr(min_length=1)] = None
    address: Optional[constr(min_length=1)] = None
    phone: Optional[constr(min_length=10)] = None

    class Config:
        from_attributes = True
        extra = Extra.forbid


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    address: Optional[str]
    email: str
    phone: str
    is_active_user: bool
    created_at: datetime
    updated_at: datetime
    user_companies: List[UserCompanyResponse]

    class Config:
        orm_mode = True
        from_attributes = True
