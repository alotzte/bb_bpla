from fastapi import FastAPI, File, UploadFile, HTTPException
from yolo import YoloModel

app = FastAPI()
model = YoloModel("weights/example.pt")

@app.post("/predict")
def predict(
    file: UploadFile = File(...)
):
    try:
        # image = Image.open(io.BytesIO(await file.read()))
        txt_path, txt_example = model.predict('qqqq')

        return {
            "txt_path": txt_path,
            "txt_example": txt_example
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
