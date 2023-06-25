from app.drawing.schemas.drawing import (
    GenerateImgRequest,
    GenerateImgResponse,
    ImagineRequest,
    ResetRequest,
    TriggerResponse,
    UploadResponse,
    UpscaleRequest,
    VariationRequest,
)
from app.drawing.services.drawing import drawing_service
from app.errors import DrawingBizError
from app.utils.exception import APPException
from app.utils.json import json_response
from app.utils.response import Response
from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/drawing",
    tags=["drawing"],
)


@router.post(
    "",
    response_model=Response,
    summary="Generate images",
)
async def generate_images(request: GenerateImgRequest):
    data = await drawing_service.generate_images(request)
    return json_response(data=data)


@router.get(
    "/result/{trigger_id}",
    response_model=Response[GenerateImgResponse],
    summary="Generate images",
)
async def fetch_trigger_result(trigger_id: str):
    data = await drawing_service.fetch_trigger_result(trigger_id)
    return json_response(data=data)


@router.post(
    "/upload",
    response_model=Response[UploadResponse],
    summary="Upload attachment",
)
async def drawing_upload(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise APPException(DrawingBizError.NOT_SUPPORT_FILE_TYPE)
    file_type = file.content_type.split("/")[-1]
    data = await drawing_service.upload_attachment(
        file.size, file_type, await file.read()
    )
    return json_response(data=data)


@router.post(
    "/imagine",
    response_model=Response[TriggerResponse],
    summary="Midjourney imagine",
)
async def drawing_imagine(request: ImagineRequest):
    data = await drawing_service.imagine_image(request)
    return json_response(data=data)


@router.post(
    "/upscale",
    response_model=Response[TriggerResponse],
    summary="Upscale images",
)
async def drawing_upscale(request: UpscaleRequest):
    """prompt - Image #1"""
    data = await drawing_service.upscale_image(request)
    return json_response(data=data)


@router.post(
    "/variation",
    response_model=Response[TriggerResponse],
    summary="Variation images",
)
async def drawing_variation(request: VariationRequest):
    """prompt - Variations"""
    data = await drawing_service.upscale_image(request)
    return json_response(data=data)


@router.post(
    "/reset",
    response_model=Response[TriggerResponse],
    summary="Reset images",
)
async def drawing_reset(request: ResetRequest):
    data = await drawing_service.reset_image(request)
    return json_response(data=data)
