from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from bot import bot, dp
from routes import root_router


async def lifespan(application: FastAPI):
    from bot import set_bot_commands_menu
    response = await bot.set_webhook(
        url="https://usable-goldfish-precious.ngrok-free.app/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logger.info(f"Webhook set response: {response}")
    await set_bot_commands_menu(bot)

    await Tortoise.init(
        db_url='sqlite:///app/bd/files/database.db',
        modules={'models': ['bd.models.user', 'bd.models.user_settings']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.mount('/static', StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
