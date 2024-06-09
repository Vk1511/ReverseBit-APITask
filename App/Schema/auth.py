from pydantic import BaseModel, Extra, constr


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
