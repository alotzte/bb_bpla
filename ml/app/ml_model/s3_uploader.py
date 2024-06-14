import boto3
from botocore.client import Config
import os
import mimetypes


ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
SPACE_NAME = os.getenv("SPACE_NAME")
REGION_NAME = os.getenv("REGION_NAME")
SERVICE_NAME = os.getenv("SERVICE_NAME")
ENDPOINT_URL = f'https://{REGION_NAME}.{SERVICE_NAME}'

s3_client = boto3.client('s3',
                         region_name=REGION_NAME,
                         endpoint_url=ENDPOINT_URL,
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         config=Config(signature_version='s3v4'))


# def upload_file_to_s3(file_name, bucket, object_name=None):
#     """
#     Загружает файл в S3-совместимое хранилище и возвращает ссылку на файл.
#     :param file_name: Имя файла для загрузки.
#     :param bucket: Название бакета (пространства).
#     :param object_name: Имя объекта в бакете. Если не указано, используется file_name.
#     :return: URL загруженного файла.
#     """
#     if object_name is None:
#         object_name = file_name
    
#     try:
#         s3_client.upload_file(file_name, bucket, object_name)
#         file_url = f"{ENDPOINT_URL}/{bucket}/{object_name}"
#         return file_url
#     except Exception as e:
#         print(f"Ошибка при загрузке файла: {e}")
#         return None


def upload_file_to_s3(file_name, bucket, data_type,
                      object_name=None, public=True):
    if object_name is None:
        object_name = os.path.basename(file_name)
    object_name = f"{data_type}/{object_name}"

    # ????
    content_type, _ = mimetypes.guess_type(file_name)
    if data_type == 'upd_videos':
        content_type = 'video/webm'
    elif content_type is not None:
        pass
    else:
        content_type = 'application/octet-stream' # Тип по умолчанию

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
        print(f"Ошибка при загрузке файла: {e}")
        return None
