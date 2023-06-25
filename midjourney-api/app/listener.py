import re
from enum import Enum

import discord
from app.drawing.schemas.drawing import GenerateImgResponse
from app.utils.logger import setup_logger
from app.utils.redis import redis_client
from discord.ext import commands

logger = setup_logger("discord_bot")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


def extract_trigger_id(content):
    pattern = r"<#(\w+?)#>"
    match = re.findall(pattern, content)
    return match[0] if match else None


class TriggerStatus(Enum):
    start = "start"
    generating = "generating"
    end = "end"
    error = "error"
    banned = "banned"
    text = "text"
    verify = "verify"


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    if message.author.id != 936929561302675456:
        return
    logger.debug(f"on_message: {message.content}")
    logger.debug(
        f"on_message embeds: {message.embeds[0].to_dict() if message.embeds else message.embeds}"
    )
    content = message.content
    trigger_id = extract_trigger_id(content) or "999"
    if not trigger_id:
        return

    msg_id = message.id
    content = message.content

    if content.find("Waiting to start") != -1:
        trigger_status = 0
    elif content.find("(Stopped)") != -1:
        trigger_status = -1
    else:
        trigger_status = 2

    data = GenerateImgResponse(
        trigger_id=trigger_id,
        trigger_status=trigger_status,
        msg_id=str(msg_id),
        content=content,
        msg_hash="",
        file_url="",
    )
    attachments = message.attachments
    if attachments:
        data.trigger_status = 2
        data.msg_hash = attachments[0].filename.split("_")[-1].split(".")[0]
        data.file_url = attachments[0].url

    redis_client.hmset(trigger_id, data.dict())
