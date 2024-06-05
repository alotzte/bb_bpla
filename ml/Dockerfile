FROM nvcr.io/nvidia/tensorrt:24.05-py3

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install huggingface huggingface_hub

RUN pip install git+https://github.com/THU-MIG/yolov10.git

RUN pip install dill

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "static/key.pem", "--ssl-certfile", "static/cert.pem"]
# uvicorn.exe main:app --host 127.0.0.1 --port 8080 --ssl-keyfile static/key.pem --ssl-certfile static/cert.pem