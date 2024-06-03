import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import WebhookInfo, BotCommand


API_TOKEN = os.getenv('API_TOKEN')
WEBHOOK_HOST = 'http://localhost:8443'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')

telegram_router = Router(name="telegram")
dp = Dispatcher()


dp.include_router(telegram_router)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)


async def set_webhook(my_bot: Bot) -> None:
    # Check and set webhook for Telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            print(e)
            # logger.error(f"Can't get webhook info - {e}")
            return

    current_webhook_info = await check_webhook()

    try:
        await bot.set_webhook(
            WEBHOOK_URL,
            secret_token=WEBHOOK_TOKEN,
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            max_connections=100,
        )

    except Exception as e:
        print(e)


async def set_bot_commands_menu(my_bot: Bot) -> None:
    # Register commands for Telegram bot (menu)
    commands = [
        BotCommand(command="/id", description="👋 Get my ID"),
    ]
    try:
        await my_bot.set_my_commands(commands)
    except Exception as e:
        print(e)


async def start_telegram():
    await set_webhook(bot)
    await set_bot_commands_menu(bot)
