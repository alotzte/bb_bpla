import os
import asyncio
import logging
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import CallbackQuery, Message, Update
from aiohttp import web

logging.basicConfig(level=logging.INFO)


class TelegramBot:

    def __init__(self):
        self.API_TOKEN = os.getenv('API_TOKEN')
        self.bot = Bot(token=self.API_TOKEN)
        self.WEBHOOK_HOST = 'http://localhost'
        self.WEBHOOK_PATH = '/webhook'
        self.WEBHOOK_URL = f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"
        self.BACKEND_URL = os.getenv('BACKEND_URL')
        self.BACKEND_PORT = os.getenv('BACKEND_PORT')
        self.TG_WEB_APP_URL = f'{self.BACKEND_URL}:{self.BACKEND_PORT}/login'
        self.dp = Dispatcher()

        self.dp.message.register(self.cmd_start, Command("settings"))

    async def cmd_start(self, message: Message) -> None:
        user_id = message.from_user.id
        if self.is_userid_in_db(user_id=user_id):
            await message.answer("Вы уже вошли в аккаунт!")

            button = InlineKeyboardButton(
                text="Настройки уведомлений",
                web_app=WebAppInfo(url=self.TG_WEB_APP_URL)
            )
            button2 = InlineKeyboardButton(
                text="☝️",
                web_app=WebAppInfo(url=self.TG_WEB_APP_URL)
            )
            markup = InlineKeyboardMarkup(inline_keyboard=[[button, button2]])

            await message.answer("Выберите опцию:", reply_markup=markup)
        else:
            await message.answer("Авторизация")

    def is_userid_in_db(self, user_id: int) -> bool:
        # TODO: подключиться к базе данных и проверить наличие пользователя в базе
        return True

    async def send_notify_to_user(self, call: CallbackQuery, user_id: int) -> None:
        photo = open(r"static/1.jpg", mode='rb')
        await self.bot.send_photo(chat_id=user_id, photo=photo)

        button_true = InlineKeyboardButton(
            text="👍",
            web_app=WebAppInfo(url=self.TG_WEB_APP_URL)
        )

        button_false = InlineKeyboardButton(
            text="👎",
            web_app=WebAppInfo(url=self.TG_WEB_APP_URL)
        )

        markup = InlineKeyboardMarkup(
            inline_keyboard=[[button_true, button_false]]
        )

        await self.bot.send_message(
            chat_id=user_id,
            text="Подтвердите найденый объект",
            reply_markup=markup
        )

    async def main(self):
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    bot_instance = TelegramBot()
    asyncio.run(bot_instance.main())
