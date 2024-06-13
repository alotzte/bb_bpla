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

VERY_SECRET_KEY = os.getenv("VERY_SECRET_KEY")


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
            future = executor.submit(self.send_data_to_tg_bot, res, photo_url, txt_url)

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

    def send_data_to_tg_bot(
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

    def draw_boxes(self, frame, boxes, classes):

        class_colors = {
            0: (255, 0, 0),  # Red
            1: (0, 255, 0),  # Green
            2: (0, 0, 255),  # Blue
            3: (255, 255, 0),  # Cyan
            4: (255, 0, 255)  # Magenta
        }
        for box, cls in zip(boxes, classes):
            color = class_colors.get(int(cls), (0, 255, 255))  # Yellow as default
            x_min, y_min, x_max, y_max = map(int, box)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
        return frame

    def sync_predict_video(self, video_path):
        fps, height, width, frames = self._get_video_info(video_path)
        object_fullname = os.path.basename(video_path)
        object_name, suffix = os.path.splitext(object_fullname)
        max_missed_frames = int(fps / 2)
        last_frame_success = False
        timestamps = []
        missed_frames = 0

        fourcc = cv2.VideoWriter_fourcc(*'VP80')    
        saved_video_path = f'/app/ml_model/{object_name}.webm'
        out = cv2.VideoWriter(saved_video_path, fourcc, fps, (width, height))

        for frame_number, r in enumerate(self.model.predict(
            video_path,
            conf=0.5,
            stream=True,
            imgsz=(240, 240), # attention!
        )):
            frame = r.orig_img 
            if len(r.boxes.xywh) > 0:
                frame = self.draw_boxes(frame, r.boxes.xyxy, r.boxes.cls)
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

        logger.warning(f'Start uploading {saved_video_path}')
        video_url = upload_file_to_s3(
            saved_video_path, 'bb-bpla', 'upd_videos'
        )
        logger.warning(f'End uploading {saved_video_path}')
        try:
            shutil.rmtree('/app/runs/detect')
        except Exception as e:
            logger.warning(f'{e}\n/app/runs/detect not found')
        os.remove(saved_video_path)
        os.remove(object_fullname)
        return video_url, timestamps

    async def predict_video(self, video_path):
        return await run_in_threadpool(self.sync_predict_video, video_path)

    async def send_async_results(self, video_path, correlation_id):
        link, timestamps = await self.predict_video(video_path)

        url = f'{BACKEND_HOST}:{BACKEND_PORT}/api/v1/upload/processed-video'

        headers = {
            "Content-Type": "application/json",
            "CorrelationId": f"{correlation_id}"
        }

        data = {
            "link": link,
            "marks": timestamps
        }
        logger.warning(data)

        ans = requests.post(
            url=url,
            headers=headers,
            json=data
        )

        logger.warning(ans)
