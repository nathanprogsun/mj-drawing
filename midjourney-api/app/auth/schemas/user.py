import re
from datetime import date, datetime

from app.auth.models.user import User
from app.utils.schema import BaseModel
from pydantic import Field, validator
from tortoise.contrib.pydantic import pydantic_model_creator

UserResponseBase = pydantic_model_creator(User)


class UserRegisterRequest(BaseModel):
    phone: str
    password: str

    @validator("phone")
    def validate_phone_number(cls, v):
        pattern = r"^\d{11}$"
        if not re.match(pattern, v):
            raise ValueError("phone number invalid")
        return v

    @validator("password")
    def validate_password(cls, v):
        min_length = 8
        max_length = 20
        pwd_len = len(v)
        pattern = r"^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[_!@#$\%\^\&\*\(\)])[0-9a-zA-Z_!@#$\%\^\&\*\(\)]"

        if pwd_len < min_length:
            raise ValueError(
                f"This password is too short,it must contain at least {min_length} character."
            )

        if pwd_len > max_length:
            raise ValueError(
                f"This password is too long,it must contain at most {max_length} character."
            )

        if not re.match(pattern, v) or " " in v:
            raise ValueError(
                "Your password must be a mixture of digits, letters and special characters (_!@#$()%^&*)."
            )

        return v


class UserCreateSchema(BaseModel):
    phone: str
    hashed_password: str


class UpdateUserLoginTime(BaseModel):
    last_login_datetime: datetime


class UserResponse(UserResponseBase):
    nickname: str = Field(None)
    email: str = Field(None)
    avatar: str = Field(None)
    hobbies: str = Field(None)
    motto: str = Field(None)
    birthdate: date = Field(None)

    class Config:
        fields = {"hashed_password": {"exclude": True}}


class UserLoginRequest(UserRegisterRequest):
    ...
