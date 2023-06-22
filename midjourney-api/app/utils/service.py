from typing import Any, Dict, Generic, Optional, TypeVar

from fastapi import HTTPException
from tortoise.contrib.pydantic.base import PydanticListModel, PydanticModel

from .db import BaseModel
from .rerequest import PaginationRequest
from .response import PaginationResponse
from .schema import BaseModel as SCHEMA

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SCHEMA)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SCHEMA)

NOT_FOUND = HTTPException(404, "Item not found")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        db_model: type[ModelType],
        res_schema: type[PydanticModel],
        multi_res_schema: type[PydanticListModel] = None,
    ):
        self.db_model = db_model
        self.res_schema = res_schema
        self.multi_res_schema = multi_res_schema

    async def get_one(self, pk: int) -> PydanticModel:
        obj = await self.db_model.filter(id=pk).first()
        if obj:
            return await self.res_schema.from_tortoise_orm(obj)
        else:
            raise NOT_FOUND

    async def get_multi(
        self, page: PaginationRequest, filters: Optional[Dict] = None
    ) -> PaginationResponse:
        queryset = (
            self.db_model.filter()
            if not filters
            else self.db_model.filter(**filters)
        )
        total = await queryset.count()
        if page.paginate:
            queryset = queryset.offset(page.offset).limit(page.limit)
        rows = await self.multi_res_schema.from_queryset(queryset)

        return PaginationResponse(
            total=total,
            rows=rows,
            **page.dict(),
        )

    async def create(
        self,
        create_schema: type[CreateSchemaType],
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> PydanticModel:
        if extra_data:
            obj = self.db_model(**dict(extra_data, **create_schema.dict()))
        else:
            obj = self.db_model(**create_schema.dict())
        await self.db_model.save(obj)
        return await self.res_schema.from_tortoise_orm(obj)

    async def update(
        self,
        pk: int,
        update_schema: type[UpdateSchemaType],
    ) -> PydanticModel:
        await self.db_model.filter(id=pk).update(**update_schema.dict())
        return await self.get_one(pk)

    async def delete(self, pk: int) -> None:
        await self.db_model(id=pk).delete()
