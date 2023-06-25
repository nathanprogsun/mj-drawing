from app.config import settings
from app.listener import bot

if __name__ == "__main__":
    bot.run(settings.DISCORD_BOT_TOKEN)
