import asyncio

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError


async def get_photo_user(user_id: int | str, bot: Bot) -> str:
    photo = await bot.get_user_profile_photos(user_id=user_id)
    photo = photo.photos[0][0].file_id
    #  print(photo)
    return photo


async def get_photo_user_bin(user_id: int | str, bot: Bot) -> str:
    photo = await bot.get_user_profile_photos(user_id=user_id)
    photo = photo.photos[0][0].file_id
    photo = await bot.download(photo)
    #  print(photo)
    return photo


class TelegramLogsHandler:
    def __init__(self):
        self.bot = None

    def setBot(self, bot: Bot):
        self.bot = bot

    def __call__(self, record):
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_emit(record))

    async def async_emit(self, record):
        try:
            chat_id = -4161154422
            await self.bot.send_message(chat_id, text=record, disable_notification=True, parse_mode=ParseMode.HTML)
        except TelegramAPIError as e:
            print(f"Error sending log message to Telegram: {e}")


logger = TelegramLogsHandler()
