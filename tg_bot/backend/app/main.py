from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel
from typing import Annotated, List
import os


# NGROK_URL = os.getenv("NGROK_URL")
BOT_TOKEN_HASH = os.getenv("API_TOKEN")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
COOKIE_NAME = os.getenv("COOKIE_NAME")
BACKEND_URL = os.getenv("BACKEND_URL")
BACKEND_PORT = os.getenv("BACKEND_PORT")

app = FastAPI()
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
