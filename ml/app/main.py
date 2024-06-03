from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io

from ml_model.yolo import YoloModel
from ml_model.exceptions.exp import ZeroObjectsDetected


class Message(BaseModel):
    message: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = YoloModel("ml_model/weights/best.pt")


@app.post(
        "/predict_photo",
        description="Кидаешь массив с изображениями и получаешь список путей фото с bbox и txt с разметкой",
        responses={
            404: {"model": Message, "description": "Zero objects detected"},
            200: {
                "description": "Successful Response",
                "content": {
                    "application/json": {
                        "example": {
                            "data": [
                                {
                                    "path_to_photo_with_bbox": "Путь к фото c bbox :str",
                                    "path_to_txt": "Путь к txt файлу :str"
                                }
                            ]
                        }
                    }
                },
            },
        },
)
async def predict_photo(
    files: List[UploadFile] = File(...)

):
    photos_data = []

    try:
        for file in files:
            image = Image.open(io.BytesIO(await file.read()))

            data = model.predict_photos(image, file.filename)
            photos_data.append(
                {
                    "path_to_photo_with_bbox": data['path_to_photo_with_bbox'],
                    "path_to_txt": data['path_to_txt']
                }
            )
        if len(photos_data) == 0:
            raise ZeroObjectsDetected
        return {
            "data": photos_data
        }

    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/predict_video')
async def predict_video(
    file: UploadFile = File(...)
):
    pass  # TODO: доделать предикт видео