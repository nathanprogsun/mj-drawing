from app.auth.schemas.user import UserLoginRequest
from app.auth.services.auth import auth_service
from app.utils.json import json_response
from app.utils.response import Response
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/token",
    response_model=Response,
    summary="Issue token",
)
async def login_access_token(request: UserLoginRequest):
    data = await auth_service.login_access_login(request)
    return json_response(data=data)


# {
#   "phone": "17612167260",
#   "password": "17612167260@t"
# }
