from typing import Optional
from pydantic import BaseModel, constr, Extra
from datetime import datetime


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    address: Optional[str]
    phone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class UserCompanyResponse(BaseModel):
    id: int
    company: CompanyResponse
    salary: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class AddUserComapny(BaseModel):
    company_id: int
    salary: int

    class Config:
        extra = Extra.forbid
