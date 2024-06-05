from bot import dp
from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


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


async def bot_send_message(
    bot: Bot,
    user_id: int,
    photo_path: str,
):
    # photo = open(
    #     photo_path,
    #     mode='rb')
    # with open(photo_path, 'rb') as photo:
    await bot.send_photo(chat_id=user_id, photo=photo_path)

    button_true = InlineKeyboardButton(
        text="👍",
        callback_data='true'
    )

    button_false = InlineKeyboardButton(
        text="👎",
        callback_data='false'
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[button_true, button_false]]
    )

    await bot.send_message(
        chat_id=user_id,
        text="Подтвердите найденый объект",
        reply_markup=markup
    )

