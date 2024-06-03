import asyncio
from aiohttp import web
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
from typing import Annotated, List
import uvicorn
from aiogram.webhook.aiohttp_server import setup_application
from bot_old import TelegramBot
from contextlib import asynccontextmanager
from bot import bot, dp
from fastapi import APIRouter, Header

from aiogram.types import Update

from bot import bot, dp
BOT_TOKEN_HASH = os.getenv("API_TOKEN")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
COOKIE_NAME = os.getenv("COOKIE_NAME")
BACKEND_URL = os.getenv("BACKEND_URL")
BACKEND_PORT = os.getenv("BACKEND_PORT")


@asynccontextmanager
async def lifespan(application: FastAPI):
    from bot import start_telegram
    await start_telegram()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HTTPSRedirectMiddleware)
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory="static"), name="static")

sample_objects = [
    {"id": 1, "name": "Object 1", "checked": True},
    {"id": 2, "name": "Object 2", "checked": False},
    {"id": 3, "name": "Object 3", "checked": True},
    {"id": 4, "name": "Object 4", "checked": True},
    {"id": 5, "name": "Object 5", "checked": True},
    {"id": 6, "name": "Object 6", "checked": False},
    {"id": 7, "name": "Object 7", "checked": True},
    {"id": 8, "name": "Object 8", "checked": True},
]


class UserRequest(BaseModel):
    user_id: str


class ObjectItem(BaseModel):
    id: int
    name: str
    checked: bool


class UpdateObjectItem(BaseModel):
    id: int
    checked: bool


class ObjectListResponse(BaseModel):
    objects: List[ObjectItem]


class UpdateObjectsRequest(BaseModel):
    user_id: str
    objects: List[UpdateObjectItem]


@app.post("/api/get_list_objects", response_model=ObjectListResponse)
async def get_list_objects(user_request: UserRequest):
    # получить список объектов на которые будут приходить уведомления
    # для данного пользователя (user_id) из базы данных

    if user_request.user_id == "user123":
        return ObjectListResponse(objects=sample_objects)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/update_list_objects")
async def update_list_objects(update_request: UpdateObjectsRequest):
    print(f"Updating objects for user {update_request.user_id}:")
    for idx, obj in enumerate(update_request.objects):
        sample_objects[idx]["checked"] = obj.checked
        print(f"Object {obj.id} checked: {obj.checked}")

    return {"status": "success"}


@app.post("/api/send_notification")
async def send_notification(user_request: UserRequest):
    # result = bot.send_notify_to_user(user_id=user_request.user_id)
    result = True
    if result:
        return {"status": "success"}
    else:
        return {"status": "error"}


@app.post('/webhook')
async def bot_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None
) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != os.getenv('API_TOKEN'):
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


@app.get("/notification-settings")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/", response_class=RedirectResponse, status_code=302)
def old():
    return "/login"


@app.get('/login')
def login(request: Request):
    response_dict = {
        "request": request,
        "backend_url": BACKEND_URL,
        "backend_port": BACKEND_PORT
    }
    print(BOT_TOKEN_HASH)
    print(response_dict)
    return templates.TemplateResponse(
        "login.html",
        response_dict
    )


