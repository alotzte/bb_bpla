import requests
import boto3
from botocore.client import Config
import os
import mimetypes
from fastapi.logger import logger

S3_TYPE = os.getenv("S3_TYPE")
if S3_TYPE == 'minio':
    ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    SPACE_NAME = os.getenv("MINIO_SPACE_NAME")
    REGION_NAME = os.getenv("MINIO_REGION_NAME")
    SERVICE_NAME = os.getenv("MINIO_SERVICE_NAME")
    ENDPOINT_URL = f'http://{REGION_NAME}{SERVICE_NAME}'

elif S3_TYPE == 'digitalocean':
    ACCESS_KEY = os.getenv("DO_ACCESS_KEY")
    SECRET_KEY = os.getenv("DO_SECRET_KEY")
    SPACE_NAME = os.getenv("DO_SPACE_NAME")
    REGION_NAME = os.getenv("DO_REGION_NAME")
    SERVICE_NAME = os.getenv("DO_SERVICE_NAME")
    ENDPOINT_URL = f'https://{REGION_NAME}.{SERVICE_NAME}'

s3_client = boto3.client('s3',
                         region_name=REGION_NAME,
                         endpoint_url=ENDPOINT_URL,
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         config=Config(signature_version='s3v4'))


def upload_file_to_s3(file_name, bucket, data_type, object_name=None, public=True, expiration=3600):
    """
    Загружает файл на S3 по URL и возвращает предписанную URL-ссылку.

    :param file_name: Путь до файла на локальной машине
    :param bucket: Название бакета
    :param data_type: Тип файла фото / видео
    :param object_name: опционально, название объекта
    :param public: опционально, публичный ли файл
    :param expiration: Время жизни предписанной URL-ссылки в секундах
    :return: URL файла в S3
    """
    if object_name is None:
        object_name = os.path.basename(file_name)
    object_name = f"{_get_current_time()}/{data_type}/{object_name}"

    content_type, _ = mimetypes.guess_type(file_name)
    if data_type == 'upd_videos':
        content_type = 'video/webm'
    elif content_type is not None:
        pass
    else:
        content_type = 'application/octet-stream'  # Тип по умолчанию

    try:
        s3_client.upload_file(
            file_name, bucket, object_name,
            ExtraArgs={'ContentType': content_type}
        )

        if public:
            s3_client.put_object_acl(
                Bucket=bucket, Key=object_name,
                ACL='public-read'
            )

        file_url = f"{ENDPOINT_URL}/{bucket}/{object_name}"
        return file_url
    except Exception as e:
        logger.warning(f"Ошибка при загрузке файла: {e}")
        return None


def download_file_from_s3(url, destination_path):
    """
    Скачивает файл из S3 по URL и сохраняет его в указанный путь.

    :param url: URL файла в S3
    :param destination_path: Локальный путь для сохранения файла
    """
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.warning(f"File downloaded: {destination_path}")
    else:
        logger.warning(f"File download failed: {response.status_code}")


def _get_current_time():
    from datetime import datetime
    now = datetime.now()
    formatted_datetime = now.strftime('%Y%m%d_%H%M%S')

    return formatted_datetime
