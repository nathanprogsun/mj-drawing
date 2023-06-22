from typing import Dict

from fastapi import FastAPI
from tortoise import BaseDBAsyncClient, fields, generate_config, timezone
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import OperationalError
from tortoise.manager import Manager
from tortoise.models import Model
from tortoise.queryset import QuerySet


def setup_db(app: FastAPI, db_url: str, modules: Dict, **kwargs):
    config = generate_config(db_url, app_modules=modules)
    config["use_tz"] = True
    register_tortoise(app, config=config, generate_schemas=False, **kwargs)


class EnabledObjectManager(Manager):
    def get_queryset(self):
        queryset_ = BaseQueryset(self._model)
        return queryset_.filter(deleted_at=None)


class BaseQueryset(QuerySet):
    async def delete(self) -> "UpdateQuery":
        update_kwargs = dict(deleted_at=timezone.now())
        return await self.update(**update_kwargs)

    async def include_archived_objects(self):
        return QuerySet(self._model).filter()

    async def force_delete(self) -> "DeleteQuery":
        return await super().delete()


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True, default=None)

    objects = EnabledObjectManager()
    all_objects = Manager()

    def __init_subclass__(cls, **kwargs):
        cls._meta.manager = EnabledObjectManager()
        super().__init_subclass__(**kwargs)

    async def delete(self, using_db: BaseDBAsyncClient | None = None) -> None:
        """
        Set deleted_at to current time to mark the object as deleted

        :param using_db: Specific DB connection to use instead of default bound

        :raises OperationalError: If object has never been persisted.
        """
        self.deleted_at = timezone.now()
        await self.save(
            force_update=True, update_fields=["deleted_at"], using_db=using_db
        )

    async def force_delete(
        self, using_db: BaseDBAsyncClient | None = None
    ) -> None:
        """
        Deletes the current model object.

        :param using_db: Specific DB connection to use instead of default bound

        :raises OperationalError: If object has never been persisted.
        """
        db = using_db or self._choose_db(True)
        if not self._saved_in_db:
            raise OperationalError("Can't delete unpersisted record")
        await self._pre_delete(db)
        await db.executor_class(model=self.__class__, db=db).execute_delete(
            self
        )
        await self._post_delete(db)

    class Meta:
        abstract = True
        ordering = ["-id"]
        manager = EnabledObjectManager()

    class PydanticMeta:
        exclude = ("deleted_at",)
