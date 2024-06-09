from sqlalchemy.orm import as_declarative, declared_attr
from typing import Any


@as_declarative()
class BaseReadOnly:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


@as_declarative()
class Base:
    pass
