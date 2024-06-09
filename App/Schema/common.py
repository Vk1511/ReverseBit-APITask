from typing import Optional, Union
from pydantic import BaseModel


class GenericResponseModel(BaseModel):
    status: bool
    message: str
    code: int
    timestamp: Optional[str]

    class Config:
        orm_mode = True


class GenericDataResponseModel(GenericResponseModel):
    data: Optional[Union[str, list, dict]]


class ErrorResponseDataSchema(BaseModel):
    message: str
    code: int

    class Config:
        orm_mode = True


class ErrorResponseModel(BaseModel):
    status: bool
    timestamp: Optional[str]
    data: ErrorResponseDataSchema

    class Config:
        orm_mode = True
