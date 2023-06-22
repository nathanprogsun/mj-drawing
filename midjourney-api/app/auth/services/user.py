from datetime import datetime

from app.auth.models.user import User
from app.auth.schemas.user import (
    UpdateUserLoginTime,
    UserCreateSchema,
    UserRegisterRequest,
    UserResponse,
)
from app.utils.security import get_password_hash
from app.utils.service import CRUDBase


class UserService(CRUDBase):
    async def user_register(self, obj_in: UserRegisterRequest) -> UserResponse:
        hashed_password = get_password_hash(obj_in.password)
        return await self.create(
            UserCreateSchema(
                hashed_password=hashed_password, phone=obj_in.phone
            )
        )

    async def update_login_time(self, u: User):
        u.last_login_datetime = None
        await u.save()


user_service = UserService(
    db_model=User,
    res_schema=UserResponse,
    multi_res_schema=UserResponse,
)
