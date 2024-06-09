from typing import Optional
from pydantic import BaseModel, constr, Extra


class UserUpdate(BaseModel):
    first_name: Optional[constr(min_length=1)] = None
    last_name: Optional[constr(min_length=1)] = None
    address: Optional[constr(min_length=1)] = None
    phone: Optional[constr(min_length=10)] = None

    class Config:
        from_attributes = True
        extra = Extra.forbid
