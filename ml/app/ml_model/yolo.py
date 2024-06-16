import os

import requests
from ultralytics import YOLO
import cv2
import shutil
from fastapi.concurrency import run_in_threadpool
from fastapi.logger import logger
from concurrent.futures import ThreadPoolExecutor
import time
from PIL import Image
import zipfile

from .s3_uploader import upload_file_to_s3, download_file_from_s3


BACKEND_HOST = os.getenv("BACKEND_HOST")
BACKEND_PORT = os.getenv("BACKEND_PORT")

FULL_PATH_TO_TXT = '/app/ml_model/temp/'
FULL_PATH_TO_VIDEO = '/app/ml_model/temp/'

VERY_SECRET_KEY = os.getenv("VERY_SECRET_KEY")


class YoloModel:
    def __init__(self, model_path):
        # model_url = 'https://bb-bpla.fra1.digitaloceanspaces.com/weights/v9c_res_dynamic.engine'
        # output_path = '/app/ml_model/weights/bb_bpla.engine'
        # download_file_from_s3(model_url, output_path)
        # self.model = YOLO(output_path)
        self.model = YOLO(model_path)

    def predict_folder(self, path):

        start_time = time.time()
        for res in self.model.predict(
            path,
            conf=0.5,
            stream=True,
            imgsz=(240, 240),  # attention!
        ):
            img, txt = os.path.join(FULL_PATH_TO_TXT, 'img'), os.path.join(FULL_PATH_TO_TXT, 'txt')
            os.makedirs(img, exist_ok=True)
            os.makedirs(txt, exist_ok=True)

            link = f"""{
                os.path.join(img, os.path.splitext(os.path.basename(res.path))[0])}.jpg"""

            txt_path = f"""{
                os.path.join(txt, os.path.splitext(os.path.basename(res.path))[0])}.txt"""

            res.save(link)
            self._save_txt(txt_path, res, is_video=False)
        end_time = time.time() - start_time

        return img, txt, int(end_time * 1000) 

    def predict_photo(self, img, filename):
        width, height = img.size
        res = self.model.predict(
            img,
            conf=0.5,
            imgsz=(320, 320),
        )  # TODO augment

        link = f"""{
            os.path.join(
                FULL_PATH_TO_TXT, 'img', os.path.splitext(filename)[0])}.jpg"""

        txt_path = f"""{
            os.path.join(
                FULL_PATH_TO_TXT, 'txt', os.path.splitext(filename)[0])}.txt"""
        os.makedirs(os.path.join(FULL_PATH_TO_TXT, 'img'), exist_ok=True)
        os.makedirs(os.path.join(FULL_PATH_TO_TXT, 'txt'), exist_ok=True)

        res[0].save(link)
        self._save_txt(txt_path, res)

        photo_url = upload_file_to_s3(link, 'bb-bpla', 'upd_photos', public=False)
        txt_url = upload_file_to_s3(txt_path, 'bb-bpla', 'upd_txts', public=False)

        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.send_photo_data_to_tg_bot, res, photo_url, txt_url)

        def log_response(future):
            try:
                response = future.result()
                logger.warning(f"tg_bot response: {response}")
            except Exception as exc:
                logger.error(f'Error sending data to TG bot: {exc}')

        future.add_done_callback(log_response)

        os.remove(link)
        os.remove(txt_path)

        return {
            'link': photo_url,
            'txt_path': txt_url,
            }

    def send_photo_data_to_tg_bot(
        self,
        res,
        photo_url,
        txt_url
    ):
        data = {
            "photo_url": photo_url,
            "txt_url": txt_url,
            "classes": res[0].boxes.cls.tolist(),
            "confs": res[0].boxes.conf.tolist(),
        }

        logger.warning(data)
        headers = {
            "Authorization": f"{VERY_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        url = 'https://usable-goldfish-precious.ngrok-free.app/api/send_messages'
        response = requests.post(url, json=data, headers=headers)
        return response

    def _save_txt(self, path, result, is_video=True):
        if is_video:
            with open(path, '+w') as file:
                for idx, prediction in enumerate(result[0].boxes.xywhn):
                    cls = int(result[0].boxes.cls[idx].item())
                    file.write(f"{cls} {prediction[0].item()} {prediction[1].item()} {prediction[2].item()} {prediction[3].item()}\n")
        else:
            with open(path, '+w') as file:
                for idx, prediction in enumerate(result.boxes.xywhn):
                    cls = int(result.boxes.cls[idx].item())
                    file.write(f"{cls} {prediction[0].item()} {prediction[1].item()} {prediction[2].item()} {prediction[3].item()}\n")

    def _get_video_info(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return fps, height, width, frames

    def _draw_boxes(self, frame, boxes, classes):

        class_colors = {
            0: (255, 0, 0),  # Red
            1: (0, 255, 0),  # Green
            2: (0, 0, 255),  # Blue
            3: (255, 255, 0),  # Cyan
            4: (255, 0, 255)  # Magenta
        }
        for box, cls in zip(boxes, classes):
            color = class_colors.get(int(cls), (0, 255, 255))
            x_min, y_min, x_max, y_max = map(int, box)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
        return frame

    def sync_predict_video(self, video_url):
        
        fps, height, width, frames = self._get_video_info(video_url)
        object_fullname = os.path.basename(video_url)
        object_name, suffix = os.path.splitext(object_fullname)
        max_missed_frames = int(fps / 2)
        last_frame_success = False
        timestamps = []
        missed_frames = 0

        fourcc = cv2.VideoWriter_fourcc(*'VP80')
        saved_video_path = f'/app/ml_model/{object_name}.webm'
        out = cv2.VideoWriter(saved_video_path, fourcc, fps, (width, height))

        start_time = time.time()
        for frame_number, r in enumerate(self.model.predict(
            video_url,
            conf=0.5,
            stream=True,
            imgsz=(240, 240), # attention!
            stream_buffer=True,
        )):
            frame = r.orig_img 
            if len(r.boxes.xywh) > 0:
                frame = self._draw_boxes(frame, r.boxes.xyxy, r.boxes.cls)
                if not last_frame_success:
                    timestamps.append((frame_number + 1) / frames)
                last_frame_success = True
                missed_frames = 0
            else:
                if last_frame_success:
                    missed_frames += 1
                    if missed_frames > max_missed_frames:
                        last_frame_success = False
                else:
                    missed_frames = 0
            out.write(frame)
        out.release()

        end_time = time.time() - start_time

        logger.warning(f'Start uploading {saved_video_path}')
        upd_video_url = upload_file_to_s3(
            saved_video_path, 'bb-bpla', 'upd_videos', public=False
        )
        logger.warning(f'End uploading {saved_video_path}')
        try:
            shutil.rmtree('/app/runs/detect')
        except Exception as e:
            logger.warning(f'{e}\n/app/runs/detect not found')
        
        try:
            os.remove(saved_video_path)
            os.remove(object_fullname)
        except Exception as e:
            logger.warning(f'{e}\n{object_fullname} not found')
        return upd_video_url, timestamps, end_time

    def sync_predict_photos_archive(self, archive_url):
        # скачать архив
        extract_folder = '/app/ml_model/temp_archive'
        os.makedirs(extract_folder, exist_ok=True)
        local_filename = self.download_file(archive_url, '/app/ml_model/temp_archive/archive.zip')
        logger.warning(f'local_filename: {local_filename}')
        # разархивировать

        self.unzip_folder(local_filename, extract_folder)
        # пройти по каждому
        inner_folder = None
        for item in os.listdir(extract_folder):
            item_path = os.path.join(extract_folder, item)
            if os.path.isdir(item_path):
                inner_folder = item_path
                break

        img_link, txt_link, processed_milliseconds = self.predict_folder(inner_folder or extract_folder)
        # заархивировать фото, txt
        img_archive_path = '/app/ml_model/temp_archive/archive_upd.zip'
        txt_archive_path = '/app/ml_model/temp_archive/archive_txt.zip'
        self.zip_folder(img_link, img_archive_path)
        self.zip_folder(txt_link, txt_archive_path)
        # загрузить на с3 фото и txt
        photo_url = upload_file_to_s3(img_archive_path, 'bb-bpla', 'upd_photos', public=False)
        txt_url = upload_file_to_s3(txt_archive_path, 'bb-bpla', 'upd_txts', public=False)
        # удалить архив

        shutil.rmtree(extract_folder)
        shutil.rmtree('/app/ml_model/temp')

        return photo_url, txt_url, processed_milliseconds

    def zip_folder(self, folder, new_zip_path):
        # photo_files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        with zipfile.ZipFile(new_zip_path, 'w') as new_zip:
            for photo in os.listdir(folder):
                photo_path = os.path.join(folder, photo)
                new_zip.write(photo_path, arcname=photo)

    def unzip_folder(self, local_filename, extract_folder):
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

    def download_file(self, url, local_filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    async def predict_video(self, video_url):
        return await run_in_threadpool(self.sync_predict_video, video_url)

    async def predict_photos_archive(self, archive_url):
        return await run_in_threadpool(self.sync_predict_photos_archive, archive_url)

    async def send_async_results(
        self,
        url,
        correlation_id,
        data_type
    ):
        if data_type == 'video':
            link, timestamps, end_time = await self.predict_video(url)

            url = f'{BACKEND_HOST}:{BACKEND_PORT}/api/v1/upload/processed-video'

            headers = {
                    "Content-Type": "application/json",
                    "CorrelationId": f"{correlation_id}"
                }

            data = {
                    "link": link,
                    "marks": timestamps,
                    "processed_milliseconds": int(end_time * 1000)
                }
            logger.warning(data)

            ans = requests.post(
                    url=url,
                    headers=headers,
                    json=data
                )

            logger.warning(f'backend answer code: {ans}')

        elif data_type == 'archive':
            photo_url, txt_url, processed_milliseconds = await self.predict_photos_archive(url)
            url = f'{BACKEND_HOST}:{BACKEND_PORT}/api/v1/upload/processed-archive'

            headers = {
                    "Content-Type": "application/json",
                    "CorrelationId": f"{correlation_id}"
                }

            data = {
                    "link": photo_url,
                    "txt": txt_url,
                    "processed_milliseconds": processed_milliseconds
                }
            logger.warning(f'data: {data}, headers: {headers}')
            ans = requests.post(
                    url=url,
                    headers=headers,
                    json=data
                )
            logger.warning(f'backend answer code archive: {ans}')
        else:
            raise Exception('unknown data type')
