from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
import requests
import os


bot = Bot(os.getenv("API_TOKEN"),
          default=DefaultBotProperties(
              parse_mode=ParseMode.HTML
          ))

dp = Dispatcher()


async def check_user_in_db(api_endpoint, user_id):
    url = f"{api_endpoint}/api/user_in_db"
    payload = {"user_id": user_id}
    response = requests.post(url, json=payload)
    return await response.json() if response.status_code == 200 else {"error": "Request failed"}


async def set_bot_commands_menu(my_bot: Bot) -> None:
    commands = [
        BotCommand(
            command="/start",
            description="👋 Запуск бота"
        ),
        BotCommand(
            command="/settings",
            description="⚙️ Настройки"
        ),
        BotCommand(
            command="/off_all_notifications",
            description="🔇 Выключить уведомления"
        ),
    ]

    try:
        await my_bot.set_my_commands(commands)
    except Exception as e:
        print(e)
