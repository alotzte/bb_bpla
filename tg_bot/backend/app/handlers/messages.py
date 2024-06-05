from .bot import dp
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Переходи в приложение для настройки оповещений: ")
    await message.answer("https://t.me/lct24_bb_bot/test/")


@dp.message(Command('settings'))
async def cmd_settings(message: Message):
    await message.answer("https://t.me/lct24_bb_bot/test/")


@dp.message(Command('off_all_notifications'))
async def cmd_off_all_notifications(message: Message): pass