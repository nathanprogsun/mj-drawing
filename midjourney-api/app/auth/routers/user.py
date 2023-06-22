from app.auth.schemas.user import UserRegisterRequest
from app.auth.services.user import user_service
from app.deps import BearerAuthentication
from app.utils.json import json_response
from app.utils.response import Response
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/register",
    response_model=Response,
    summary="",
)
async def user_register(request: UserRegisterRequest):
    data = await user_service.user_register(request)
    return json_response(data=data)


@router.get(
    "/{user_id}",
    response_model=Response,
    summary="",
)
async def user_detail(
    user_id: int,
    token: str = Depends(BearerAuthentication),
):
    data = await user_service.get_one(user_id)
    return json_response(data=data)
