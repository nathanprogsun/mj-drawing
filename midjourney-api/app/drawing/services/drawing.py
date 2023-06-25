import json
import random
import uuid
from typing import Any, Dict

import aiohttp
from app.config import settings
from app.drawing.enums import ScaleCategory, TriggerType
from app.drawing.schemas.drawing import (
    GenerateImgRequest,
    GenerateImgResponse,
    ImagineRequest,
    ResetRequest,
    TriggerPayload,
    TriggerResponse,
    UploadResponse,
    UpscaleRequest,
    VariationRequest,
)
from app.errors import DrawingBizError
from app.utils.exception import APPException
from app.utils.http import FetchMethod, fetch, fetch_json
from app.utils.redis import redis_client


class DrawingService:
    TRIGGER_URL = "https://discord.com/api/v9/interactions"
    UPLOAD_ATTACHMENT_URL = f"https://discord.com/api/v9/channels/{settings.DISCORD_CHANNEL_ID}/attachments"
    SEND_MESSAGE_URL = f"https://discord.com/api/v9/channels/{settings.DISCORD_CHANNEL_ID}/messages"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": settings.DISCORD_USER_TOKEN,
    }

    async def trigger(self, payload: Dict[str, Any]):
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30), headers=self.HEADERS
        ) as session:
            return await fetch(
                session, self.TRIGGER_URL, data=json.dumps(payload)
            )

    async def generate_images(self, obj_in: GenerateImgRequest):
        params = f" --ar {ScaleCategory.get_value(obj_in.scale_category)} "
        if obj_in.model.model_type:
            if obj_in.model.text_match:
                params += f"--q {obj_in.model.text_match} "
            if obj_in.model.img_processing:
                params += f"--iw {obj_in.model.img_processing} "

        return await self.imagine_image(
            ImagineRequest(
                prompt=obj_in.description + params,
                file_url=obj_in.reference_url,
            )
        )

    async def fetch_trigger_result(
        self, trigger_id: str
    ) -> GenerateImgResponse:
        if redis_client.exists(trigger_id):
            result = redis_client.hgetall(trigger_id)
            result_dict = {
                key.decode(): value.decode() for key, value in result.items()
            }
            return GenerateImgResponse(**result_dict)
        return GenerateImgResponse(trigger_id=trigger_id, trigger_status=0)

    @staticmethod
    def pre_process_prompt(trigger_id: str, obj_in: ImagineRequest):
        return f"{obj_in.file_url + ' ' if obj_in.file_url else ''}<#{trigger_id}#>{obj_in.prompt}"

    async def imagine_image(self, obj_in: ImagineRequest):
        trigger_id = self.generate_trigger_id()
        prompt = self.pre_process_prompt(trigger_id, obj_in)
        print("prompt-->", prompt)
        version = "1118961510123847772"
        payload = TriggerPayload(
            type=TriggerType.IMAGINE.value,
            session_id=self.generate_session_id(),
            nonce=self.generate_nonce(),
            data={
                "version": version,
                "id": "938956540159881230",
                "name": "imagine",
                "type": 1,
                "options": [{"type": 3, "name": "prompt", "value": prompt}],
                "application_command": {
                    "id": "938956540159881230",
                    "application_id": settings.DISCORD_APPLICATION_ID,
                    "version": version,
                    "default_permission": True,
                    "default_member_permissions": None,
                    "type": 1,
                    "nsfw": False,
                    "name": "imagine",
                    "description": "Create images with Midjourney",
                    "dm_permission": True,
                    "contexts": [0, 1, 2],
                    "options": [
                        {
                            "type": 3,
                            "name": "prompt",
                            "description": "The prompt to imagine",
                            "required": True,
                        }
                    ],
                },
                "attachments": [],
            },
        )
        await self.trigger(payload.dict())
        return TriggerResponse(
            trigger_id=trigger_id,
            trigger_type="imagine",
        )

    async def upscale_image(self, obj_in: UpscaleRequest):
        kwargs = {
            "message_flags": 0,
            "message_id": obj_in.msg_id,
        }
        payload = TriggerPayload(
            type=TriggerType.UPSCALE.value,
            session_id=self.generate_session_id(),
            nonce=self.generate_nonce(),
            data={
                "component_type": 2,
                "custom_id": f"MJ::JOB::upsample::{obj_in.index}::{obj_in.msg_hash}",
            },
        ).dict()
        payload.update(kwargs)
        await self.trigger(payload)

    async def variation_image(self, obj_in: VariationRequest):
        kwargs = {
            "message_flags": 0,
            "message_id": obj_in.msg_id,
        }
        payload = TriggerPayload(
            type=TriggerType.VARIATION.value,
            session_id=self.generate_session_id(),
            nonce=self.generate_nonce(),
            data={
                "component_type": 2,
                "custom_id": f"MJ::JOB::variation::{obj_in.index}::{obj_in.msg_hash}",
            },
        ).dict()
        payload.update(kwargs)
        await self.trigger(payload)

    async def reset_image(self, obj_in: ResetRequest):
        kwargs = {
            "message_flags": 0,
            "message_id": obj_in.msg_id,
        }
        payload = TriggerPayload(
            type=TriggerType.RESET.value,
            session_id=self.generate_session_id(),
            nonce=self.generate_nonce(),
            data={
                "component_type": 2,
                "custom_id": f"MJ::JOB::reroll::0::{obj_in.msg_hash}::SOLO",
            },
        ).dict()
        payload.update(kwargs)
        await self.trigger(payload)

    async def put_attachment(self, url: str, image: bytes):
        headers = {"Content-Type": "image/png"}
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30), headers=headers
        ) as session:
            return await fetch(
                session, url, data=image, method=FetchMethod.put
            )

    async def upload_attachment(
        self,
        file_size: int,
        file_type: str,
        image: bytes,
    ) -> UploadResponse:
        trigger_id = self.generate_trigger_id()
        filename = trigger_id + "." + file_type
        payload = {
            "files": [
                {"filename": filename, "file_size": file_size, "id": "0"}
            ]
        }
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30), headers=self.HEADERS
        ) as session:
            upload_attachment_resp = await fetch_json(
                session, self.UPLOAD_ATTACHMENT_URL, data=json.dumps(payload)
            )
            if not upload_attachment_resp or not upload_attachment_resp.get(
                "attachments"
            ):
                raise APPException(DrawingBizError.UPLOAD_ATTACHMENT_ERR)
            _attachment = upload_attachment_resp["attachments"][0]

            await self.put_attachment(_attachment["upload_url"], image)

            _attachment.pop("upload_url")
            filename = _attachment.pop("upload_filename")
            _attachment["uploaded_filename"] = filename
            _attachment["filename"] = filename.split("/")[-1]
            sent_msg_payload = dict(
                attachments=[_attachment],
                channel_id=settings.DISCORD_CHANNEL_ID,
                nonce=self.generate_nonce(),
                sticker_ids=[],
                type=0,
                content="",
            )
            response = await fetch_json(
                session,
                self.SEND_MESSAGE_URL,
                data=json.dumps(sent_msg_payload),
            )
            attachment = response["attachments"][0]
        return UploadResponse(
            trigger_id=trigger_id,
            filename=attachment.get("filename"),
            file_url=attachment.get("url"),
        )

    @staticmethod
    def generate_nonce():
        digits = [random.randint(0, 9) for _ in range(18)]
        last_digit = random.randint(1, 9)
        return "".join(map(str, digits)) + str(last_digit)

    @staticmethod
    def generate_trigger_id():
        return uuid.uuid4().hex[:19]

    @staticmethod
    def generate_session_id():
        return uuid.uuid4().hex


drawing_service = DrawingService()
