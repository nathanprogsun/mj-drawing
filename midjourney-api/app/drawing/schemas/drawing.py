from typing import Any

from app.config import settings
from app.drawing.enums import ScaleCategory
from app.utils.schema import BaseModel
from pydantic import Field


class GenerateModel(BaseModel):
    model_type: int = Field(default=0, description="0->free; 1->custom")
    text_match: float = Field(default=0)
    img_processing: float = Field(default=0)


class GenerateImgRequest(BaseModel):
    description: str = Field(max_length=300)
    model: GenerateModel
    scale_category: str = Field(description=f"{ScaleCategory.get_names()}")
    reference_url: str = Field(None)


class GenerateImgResponse(BaseModel):
    trigger_id: str
    trigger_status: int = Field(
        default=0, description="-1->fail 0->start 1->generating 2->end"
    )
    trigger_content: str = Field(default="")
    msg_id: str = Field(default="")
    msg_hash: str = Field(default="")
    file_url: str = Field(default="")


class TriggerPayload(BaseModel):
    type: int
    application_id: str = Field(default=settings.DISCORD_APPLICATION_ID)
    guild_id: str = Field(default=settings.DISCORD_GUILD_ID)
    channel_id: str = Field(default=settings.DISCORD_CHANNEL_ID)
    session_id: str
    data: Any
    nonce: str


class TriggerResponse(BaseModel):
    trigger_id: str
    trigger_type: str


class UploadResponse(BaseModel):
    trigger_id: str
    filename: str
    file_url: str


class ImagineRequest(BaseModel):
    prompt: str
    file_url: str = Field(None)


class UpscaleRequest(BaseModel):
    trigger_id: str
    index: int
    msg_id: str
    msg_hash: str


class VariationRequest(UpscaleRequest):
    ...


class ResetRequest(BaseModel):
    trigger_id: str
    msg_id: str
    msg_hash: str
