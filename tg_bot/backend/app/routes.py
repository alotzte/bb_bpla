import os

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.logger import logger
from fastapi.responses import RedirectResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

from bot import bot, dp
from aiogram.types import Update

from handlers.messages import bot_send_message
from bd.crud import UserCRUD, UserSettingsCRUD
from data_models import (ObjectListResponse, MLDataRequest,
                         UserRequest, UpdateObjectsRequest,
                         MessageData)


VERY_SECRET_KEY = os.getenv("VERY_SECRET_KEY")

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")


@root_router.get("/", response_class=RedirectResponse, status_code=302)
async def root(request: Request):
    return '/notification-settings'


@root_router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    update = Update.model_validate(data, context={"bot": "bot"})
    # update = Update(**data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}


@root_router.get('/login')
def login(request: Request):
    response_dict = {
        "request": request,
    }
    return templates.TemplateResponse(
        "login.html",
        response_dict
    )


@root_router.get("/notification-settings")
def read_root(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})


async def get_default_settings():
    sample_objects = [
        {"id": 1, "name": "БПЛА коптерного типа", "checked": True, "inputData": 50},
        {"id": 2, "name": "Самолет", "checked": False, "inputData": 50},
        {"id": 3, "name": "Вертолет", "checked": True, "inputData": 50},
        {"id": 4, "name": "Птица", "checked": True, "inputData": 50},
        {"id": 5, "name": "БПЛА самолетного типа", "checked": True, "inputData": 50},
    ]
    return sample_objects


@root_router.post("/api/user_in_db")
async def is_user_in_db(user_request: UserRequest):
    if await UserCRUD.user_exists(user_request.user_id):
        return {"success": "ok"}
    else:
        return {"success": "error"}


@root_router.get("/api/get_user_id")
async def get_user_id():
    return {"userId": "1"}


@root_router.post("/api/get_list_objects", response_model=ObjectListResponse)
async def get_list_objects(user_request: UserRequest):
    logger.warning(user_request.user_id)
    if await UserCRUD.user_exists(user_request.user_id):
        settings = await UserSettingsCRUD.get_user_settings_by_telegram_id(
            user_request.user_id
        )
        return ObjectListResponse(objects=settings.settings)
    else:
        await UserCRUD.create_user(user_request.user_id, 'test')
        settings = await get_default_settings()
        await UserSettingsCRUD.create_user_settings(
            user_request.user_id, settings
        )
        return ObjectListResponse(objects=settings)


@root_router.post("/api/update_list_objects")
async def update_list_objects(update_request: UpdateObjectsRequest):
    print(f"Updating objects for user {update_request.user_id}:")
    if await UserCRUD.user_exists(update_request.user_id):
        settings = await UserSettingsCRUD.get_user_settings_by_telegram_id(
            update_request.user_id
        )
        for idx, obj in enumerate(update_request.objects):
            settings.settings[idx]["checked"] = obj.checked
            settings.settings[idx]["inputData"] = obj.inputData

        await UserSettingsCRUD.update_settings_by_telegram_id(
            update_request.user_id,
            settings.settings
        )
        return {"status": "success"}


@root_router.post("/api/send_messages")
async def send_messages(
    request: Request,
    message_data: MessageData,
    background_tasks: BackgroundTasks
):
    authorization: str = request.headers.get("Authorization")
    if authorization != VERY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Иди лесом")
    
    background_tasks.add_task(
        bot_send_messages,
        message_data.photo_url,
        message_data.txt_url,
        message_data.classes,
        message_data.confs
    )
    return {"status": "success"}


async def bot_send_messages(
    photo_url,
    txt_url,
    classes,
    confs,
):
    for data in await UserSettingsCRUD.get_all_users_settings():
        if data['telegram_id'] != 1:
            for i in range(len(classes)):
                logger.warning(int(classes[i]) + 1)
                logger.warning(confs)
                settings_conf = await get_conf_by_class(data['telegram_id'], int(classes[i]))
                if confs[i]*100 <= settings_conf:
                    await bot_send_message(
                        bot,
                        data['telegram_id'],
                        photo_path=photo_url,
                        predicted_class=int(classes[i])
                    )
                    break


async def get_conf_by_class(telegram_id, idx):
    settings = await UserSettingsCRUD.get_user_settings_by_telegram_id(
        telegram_id
    )
    logger.warning(settings.settings[idx])
    if settings.settings[idx]['checked']:
        return int(settings.settings[idx]['inputData'])
    return 0
