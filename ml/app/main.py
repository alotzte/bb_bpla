import json
import io
import os
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tempfile import NamedTemporaryFile
from PIL import Image
import requests

from ml_model.yolo import YoloModel
from ml_model.exceptions.exp import ZeroObjectsDetected
from ml_model.models.response_models import (PredictPhotosResponse,
                                             PredictVideoResponse)


class Message(BaseModel):
    message: str = 'Не найдено ни одного объекта'


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = YoloModel("ml_model/weights/yolov10n.pt")

class UrlsModel(BaseModel):
    urls: List[str]

@app.post(
    "/ml/predict_photos",
    description=(
        'Принимает массив с ссылками c s3 на изображения  (например '
        '["https://bb-bpla.fra1.digitaloceanspaces.com/zidane.jpg", '
        '"https://bb-bpla.fra1.digitaloceanspaces.com/bus.jpg"] ) и возвращает массив ссылок на фото и txt на s3'
    ),
    responses={
        404: {
            "model": Message,
            "description": "Zero objects detected"
        },
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "predicted_data": [
                            {
                                "link": "ссылка на фото на s3",
                                "txt_path": "ссылка на txt на s3",
                            }
                        ],
                        "type": "images"
                    }
                }
            }
        }
    },
    response_model=PredictPhotosResponse
)
async def predict_photos(urls: UrlsModel):
    photos_data = []

    try:
        for url in urls.urls:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            filename = url.split("/")[-1]
            data = model.predict_photo(img, filename)
            photos_data.append(
                {
                    "link": data['link'],
                    "txt_path": data['txt_path']
                }
            )

        if len(photos_data) == 0:
            raise ZeroObjectsDetected

        return {
            "predicted_data": photos_data,
            "type": "images"
        }

    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/ml/predict_video",
    description=('Принимает: ссылку с s3 на видео (например "https://bb-bpla.fra1.digitaloceanspaces.com/test_video.mp4" )\n'
                 'Возвращает: ссылку с s3 на видео и временные отметки'),
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "link": "ссылка на видео на s3",
                        "marks": ["метка 1", "метка 2"],
                        "type": "video",
                    }
                }
            },
        },
        404: {
            "model": Message,
            "description": "Zero objects detected"
        },
    },
    response_model=PredictVideoResponse
)
async def predict_video(
    url: str = Form(...)
):
    # Удаляем кавычки из начала и конца строки, если они есть
    if url.startswith('"') and url.endswith('"'):
        url = url[1:-1]

    # Проверяем доступность URL
    try:
        response = requests.head(url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"URL {url} is not accessible.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error accessing URL {url}: {str(e)}")

    file_path = url
    try:
        # Предположим, что модель и метод model.predict_video уже определены где-то в вашем коде
        link, timestamps = model.predict_video(file_path)
        if len(timestamps) == 0:
            raise ZeroObjectsDetected
    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        return {"message": f"There was an error processing the file:\n{str(e)}"}

    return {
        'link': link,
        'marks': timestamps,
        'type': 'video'
    }