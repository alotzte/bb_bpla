import os

import requests
from ultralytics import YOLOv10
import cv2
import shutil
from fastapi.concurrency import run_in_threadpool
from fastapi.logger import logger
from concurrent.futures import ThreadPoolExecutor

from .s3_uploader import upload_file_to_s3


BACKEND_HOST = os.getenv("BACKEND_HOST")
BACKEND_PORT = os.getenv("BACKEND_PORT")

FULL_PATH_TO_TXT = '/app/ml_model/temp/'
FULL_PATH_TO_VIDEO = '/app/ml_model/temp/'


class YoloModel:
    def __init__(self, model_path):
        self.model = YOLOv10(model_path)

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

        # TODO: если объект нашелся
        res[0].save(link)
        # res[0].save_txt(txt_path)

        self._save_txt(txt_path, res)

        photo_url = upload_file_to_s3(link, 'bb-bpla', 'upd_photos')
        txt_url = upload_file_to_s3(txt_path, 'bb-bpla', 'upd_txts')

        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.send_data_to_tg_bot, res, photo_url)

        # Логируем ответ, когда задача завершится
        def log_response(future):
            try:
                response = future.result()
                logger.warning(response)
            except Exception as exc:
                logger.error(f'Error sending data to TG bot: {exc}')

        future.add_done_callback(log_response)

        
        # TODO: проверить загрузилось ли?
        os.remove(link)
        os.remove(txt_path)
        return {
            'link': photo_url,
            'txt_path': txt_url,
        }

    def send_data_to_tg_bot(self, res, photo_url):
        data = {
            "photo_url": photo_url,
            "classes": res[0].boxes.cls.tolist(),
            "confs": res[0].boxes.conf.tolist(),
        }

        logger.warning(data)
        headers = {
            "Authorization": "6e80bf7385f34085dc3ac9f115d08d36bd8a308bcf2b1c8f0e282487a7ba0d50",
            "Content-Type": "application/json"
        }

        url = 'https://usable-goldfish-precious.ngrok-free.app/api/send_messages'
        response = requests.post(url, json=data, headers=headers)
        return response

    def _save_txt(self, path, result):
        with open(path, '+w') as file:
            for idx, prediction in enumerate(result[0].boxes.xywhn):
                cls = int(result[0].boxes.cls[idx].item())
                file.write(f"{cls} {prediction[0].item()} {prediction[1].item()} {prediction[2].item()} {prediction[3].item()}\n")

    def _get_video_info(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return fps, height, width, frames

    def sync_predict_video(self, video_path):
        fps, height, width, frames = self._get_video_info(video_path)
        object_fullname = os.path.basename(video_path)
        object_name, suffix = os.path.splitext(object_fullname)
        max_missed_frames = int(fps / 2)
        last_frame_success = False
        timestamps = []
        missed_frames = 0

        for frame_number, r in enumerate(self.model.predict(
            video_path,
            conf=0.5,
            save=True,
            stream=True,
            imgsz=(320, 320), # attention!
        )):

            if len(r.boxes.xywh) > 0:
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

        saved_video_path = f'/app/runs/detect/predict/{object_name}.avi'
        video_url = upload_file_to_s3(
            saved_video_path, 'bb-bpla', 'upd_videos'
        )
        shutil.rmtree('/app/runs/detect')
        os.remove(object_fullname)
        return video_url, timestamps

    async def predict_video(self, video_path):
        return await run_in_threadpool(self.sync_predict_video, video_path)

    async def send_async_results(self, video_path):
        link, timestamps = self.predict_video(video_path)
        video_data = {
            "link": link,
            "marks": timestamps
        }
        req = {
            "predicted_data": video_data,
            "type": "videos"
        }

        requests.post(f'http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/?',
                      json=req)
        # return {
        #     "predicted_data": video_data,
        #     "type": "videos"
        # }
