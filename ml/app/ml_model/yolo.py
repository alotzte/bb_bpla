from datetime import datetime, timedelta
import os
from ultralytics import YOLOv10
import cv2
import shutil

from .s3_uploader import upload_file_to_s3

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

        # TODO: создать папки
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
        # TODO: проверить загрузилось ли?
        os.remove(link)
        os.remove(txt_path)
        return {
            'link': photo_url,
            'txt_path': txt_url,
            # 'confidence':
        }

    def _save_txt(self, path, result):
        with open(path, '+w') as file:
            for idx, prediction in enumerate(result[0].boxes.xywhn):
                cls = int(result[0].boxes.cls[idx].item())
                # Write line to file in YOLO label format : cls x y w h
                file.write(f"{cls} {prediction[0].item()} {prediction[1].item()} {prediction[2].item()} {prediction[3].item()}\n")

    def get_video_info(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return fps, height, width, frames

    def predict_video(self, video_path):
        fps, height, width, frames = self.get_video_info(video_path)
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
        video_url = upload_file_to_s3(saved_video_path, 'bb-bpla', 'upd_videos')
        shutil.rmtree('/app/runs/detect')
        os.remove(object_fullname)
        return video_url, timestamps
