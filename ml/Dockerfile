FROM nvcr.io/nvidia/tensorrt:22.12-py3

WORKDIR /app

COPY /app/requirements.txt .

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY ./app .

RUN pip install onnx

COPY /app/ml_model/predictor.py /usr/local/lib/python3.8/dist-packages/ultralytics/engine/predictor.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "static/key.pem", "--ssl-certfile", "static/cert.pem"]
# uvicorn.exe main:app --host 127.0.0.1 --port 8080 --ssl-keyfile static/key.pem --ssl-certfile static/cert.pem
