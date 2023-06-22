from datetime import timedelta
from typing import Dict

from app.auth.schemas.user import UserLoginRequest
from app.auth.services.user import user_service
from app.config import settings
from app.errors import UserBizError
from app.utils import security
from app.utils.exception import APPException


class AuthService:
    async def login_access_login(self, obj_in: UserLoginRequest) -> Dict:
        u = await user_service.db_model.filter(phone=obj_in.phone).first()
        if not u:
            raise APPException(UserBizError.USER_NOT_FOUND)

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token_payload = {
            "id": u.id,
            "phone": u.phone,
        }
        payload = {
            "access_token": security.create_access_token(
                token_payload, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
        await user_service.update_login_time(u)
        return payload


auth_service = AuthService()
