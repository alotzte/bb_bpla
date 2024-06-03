import os
import asyncio
import logging
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import CallbackQuery, Message
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)

BACKEND_URL = os.getenv('BACKEND_URL')
BACKEND_PORT = os.getenv('BACKEND_PORT')
# TG_WEB_APP_URL = 'https://t.me/lct24_bb_bot/test'
TG_WEB_APP_URL = '{MAIN_URL}:{BACKEND_PORT}/login'
dp = Dispatcher()


@dp.message(Command("settings"))
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    if is_userid_in_db(user_id=user_id):
        await message.answer("Вы уже вошли в аккаунт!")

        button = InlineKeyboardButton(
            text="Настройки уведомлений",
            web_app=WebAppInfo(url=TG_WEB_APP_URL)
        )
        button2 = InlineKeyboardButton(
            text="☝️",
            web_app=WebAppInfo(url=TG_WEB_APP_URL)
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[[button, button2]])

        await message.answer("Выберите опцию:", reply_markup=markup)
    else:
        await message.answer("Авторизация")

    await message.answer("Hello!")


def is_userid_in_db(
        user_id: int
) -> bool:
    # TODO: подключиться к базе данных и проверить наличие пользователя в базе
    return True


async def send_notify_to_user(call: CallbackQuery, user_id: int) -> None:
    photo = open(
        r"C:\Users\ifonya\Pictures\Screenshots\уапуауаукипаипкупв.png",
        mode='rb')
    await bot.send_photo(chat_id=user_id, photo=photo)

    button_true = InlineKeyboardButton(
        text="👍",
        web_app=WebAppInfo(url=TG_WEB_APP_URL)
    )

    button_false = InlineKeyboardButton(
        text="👎",
        web_app=WebAppInfo(url=TG_WEB_APP_URL)
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[button_true, button_false]]
    )

    await bot.send_message(
        chat_id=user_id,
        text="Подтвердите найденый объект",
        reply_markup=markup
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
