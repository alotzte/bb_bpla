import os
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# import aiofiles
from tempfile import NamedTemporaryFile
# import asyncio
from PIL import Image
import io
import cv2

from ml_model.yolo import YoloModel
from ml_model.exceptions.exp import ZeroObjectsDetected


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
        "/ml/predict_photo",
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
                                    "upd_photo_path": "Путь к фото c bbox",
                                    "txt_path": "Путь к txt файлу"
                                }
                            ]
                        }
                    }
                },
            },
        },
)
async def predict_photo(
    files: List[UploadFile] = File(description='Загрузка фото')
):
    photos_data = []
    # TODO: добавить ограничение на расширения
    try:
        for file in files:
            image = Image.open(io.BytesIO(await file.read()))

            data = model.predict_photos(image, file.filename)
            photos_data.append(
                {
                    "upd_photo_path": data['upd_photo_path'],
                    "txt_path": data['txt_path']
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


# @app.post(
#     '/ml/predict_video_async',
# )
# async def predict_video(
#     file: UploadFile = File(...)
# ):
#     try:
#         async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
#             try:
#                 contents = await file.read()
#                 await temp.write(contents)
#             except Exception:
#                 return {"message": "There was an error uploading the file"}
#             finally:
#                 await file.close()

#         res = await run_in_threadpool(process_video, temp.name)  # Pass temp.name to VideoCapture()
#     except Exception:
#         return {"message": "There was an error processing the file"}
#     finally:
#         os.remove(temp.name)

#     return res


@app.post(
    "/ml/predict_video",
    description="Кидаешь видео, получаешь путь к видео и список интервалов",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "upd_video_path": "Путь к видео c bbox",
                        "intervals": "Интервалы (начало_эпизода:конец_эпизода)"
                    }
                }
            },
        },
        404: {
            "model": Message,
            "description": "Zero objects detected"
        },
    })
def predict_video(file: UploadFile = File(...)):
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
        # print(temp.name)
        intervals = model.predict_video(temp.name)
        if len(intervals) == 0:
            raise ZeroObjectsDetected

    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        return {"message": f"There was an error processing the file:\n{str(e)}"}
    finally:
        os.remove(temp.name)

    return {
        'upd_video_path': file.filename,
        'intervals': intervals
    }
