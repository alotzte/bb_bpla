import io

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from PIL import Image
import requests

from ml_model.yolo import YoloModel
from ml_model.exceptions.exp import ZeroObjectsDetected
from ml_model.models.response_models import (
    PredictPhotosResponse,
    UrlsModel,
)


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
# model = YoloModel("ml_model/weights/yolov10n.pt")
model = YoloModel("ml_model/weights/best_after_clean_init_dataset.pt")


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
async def predict_photos(
    urls: UrlsModel,
):

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
)
def predict_video(
    urls: UrlsModel,
    background_tasks: BackgroundTasks,
):
    for url in urls.urls:
        if url.startswith('"') and url.endswith('"'):
            url = url[1:-1]

        background_tasks.add_task(model.send_async_results, url)

    return {
        'predicted_status': 'in_progress',
        'type': 'video'
    }
