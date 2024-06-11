from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
import os


bot = Bot(os.getenv("TG_BOT_TOKEN"),
          default=DefaultBotProperties(
              parse_mode=ParseMode.HTML
          ))

dp = Dispatcher()
router = Router()
dp.include_router(router)


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
