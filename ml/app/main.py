from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from ml_model.yolo import YoloModel
from ml_model.exceptions.exp import ZeroObjectsDetected
import io


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
model = YoloModel("ml/app/ml_model/weights/best.pt")


@app.post(
        "/predict",
        description="Кидаешь изображение получаешь txt с разметкой",
        responses={
            404: {"model": Message, "description": "Zero objects detected"},
            200: {
                "description": "Successful Response",
                "content": {
                    "application/json": {
                        "example": {
                            "txt_path": "Путь к txt файлу :str",
                            "txt_data": "Содержимое txt файла :str"
                        }
                    }
                },
            },
        },
)
async def predict(
    file: UploadFile = File(...)

):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        obj_class, obj_coords = model.predict(media=image)
        if obj_class is None:
            raise ZeroObjectsDetected
        return {
            "obj_class": obj_class,
            "obj_coords": obj_coords
        }
    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
