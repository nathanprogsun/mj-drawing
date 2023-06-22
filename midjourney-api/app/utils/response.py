from typing import Generic, List, Optional, TypeVar, Union

from pydantic import Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    code: int = Field(
        default=0,
        title="code",
        description="""
        0-> no error
        not 0-> business error
        """,
    )
    message: str = Field(
        default="SUCCESS",
        title="description",
        description="error message uppercase and underline",
    )
    data: T = Field(
        default=None,
        title="data",
    )


class PaginationResponse(GenericModel, Generic[T]):
    total: int = Field(
        default=0, title="total", description="The records count"
    )
    page_number: int = Field(
        default=1, title="page_number", description="page size from 1"
    )
    page_size: int = Field(
        default=20, title="page_size", description="row size for a page"
    )
    rows: Optional[Union[List[T], T]] = Field(
        default=None, title="rows", description="The data list"
    )
