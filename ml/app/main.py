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
from ml_model.models.response_models import (PredictPhotoResponse,
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


@app.post(
    "/ml/predict_photos",
    description="Кидаешь массив с изображениями и получаешь список путей фото с bbox и txt с разметкой",
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
                        "data": [
                            {
                                "link": "ссылка на фото на s3",
                                "txt_path": "ссылка на txt на s3",
                            }
                        ],
                        "type": "images"
                    }
                }
            },
        },
    },
    response_model=PredictPhotoResponse
)
async def predict_photos(
    files: Optional[List[UploadFile]] = File(None),
    urls: Optional[str] = Form(None)
):
    if not files and not urls:
        raise HTTPException(status_code=400, detail="Either files or urls must be provided")

    photos_data = []

    try:
        if files:
            for file in files:
                image = Image.open(io.BytesIO(await file.read()))
                data = model.predict_photo(image, file.filename)
                photos_data.append(
                    {
                        "link": data['link'],
                        "txt_path": data['txt_path']
                    }
                )

        if urls:
            try:
                urls_list = json.loads(urls)  # Парсим JSON строку в список
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format for urls")

            for url in urls_list:
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

        else:
            ...
            # TODO: отправлять в тг бота

        return {
            "data": photos_data,
            "type": "images"
        }

    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/ml/predict_video",
    description="Кидаешь видео, получаешь путь к видео и список интервалов",
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
async def predict_video(file: UploadFile = File(None), url: str = Form(None)):
    if file is None and url is None:
        raise HTTPException(status_code=400, detail="Either file or url must be provided")

    if file:
        suffix = os.path.splitext(file.filename)[1]
        temp = NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            try:
                contents = file.file.read()
                with temp as f:
                    f.write(contents)
            except Exception:
                return {"message": "There was an error uploading the file"}
            finally:
                file.file.close()
            file_path = temp.name
        except Exception as e:
            return {"message": f"There was an error processing the file:\n{str(e)}"}
    else:
        file_path = url

    try:
        link, timestamps = model.predict_video(file_path)
        if len(timestamps) == 0:
            raise ZeroObjectsDetected
    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        return {"message": f"There was an error processing the file:\n{str(e)}"}
    finally:
        if file:
            os.remove(file_path)

    logger.warn(timestamps)
    return {
        'link': link,
        'marks': timestamps,
        'type': 'video'
    }
