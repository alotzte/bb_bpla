from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml_model.yolo import YoloModel
from ml_model.exceptions.exp import ZeroObjectsDetected


class Message(BaseModel):
    message: str


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = YoloModel("weights/example.pt")


@app.post(
        "/predict",
        description="Кидаешь изображение получаешь txt с разеткой",
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
def predict(
    file: UploadFile = File(...),
    message: str = Query(max_length=20),
    
):
    try:
        # image = Image.open(io.BytesIO(await file.read()))
        txt_path, txt_example = model.predict(media=message)
        if txt_example is None:
            raise ZeroObjectsDetected
        return {
            "txt_path": txt_path,
            "txt_data": txt_example
        }
    except ZeroObjectsDetected as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




