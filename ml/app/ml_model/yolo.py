from datetime import datetime, timedelta
import os
from ultralytics import YOLOv10
import cv2


FULL_PATH_TO_TXT = '/app/ml_model/results/'
FULL_PATH_TO_VIDEO = '/app/ml_model/results/'


class YoloModel:
    def __init__(self, model_path):
        self.model = YOLOv10(model_path)

    def predict_photos(self, img, filename):
        width, height = img.size
        res = self.model.predict(
            img,
            conf=0.5,
            imgsz=(height, width),
        )  # TODO augment

        # TODO: создать папки
        upd_photo_path = f"""{
            os.path.join(
                FULL_PATH_TO_TXT, 'img', os.path.splitext(filename)[0])}.jpg"""

        txt_path = f"""{
            os.path.join(
                FULL_PATH_TO_TXT, 'txt', os.path.splitext(filename)[0])}.txt"""

        # TODO: Продумать куда сохранять
        res[0].save(upd_photo_path)
        res[0].save_txt(txt_path)
        # TODO: Проверить сохранение

        return {
            'upd_photo_path': upd_photo_path,
            'txt_path': txt_path
        }

    def predict_video(self, video_path):
        last_frame_success = False
        fps = self.get_video_info(video_path)
        intervals = {}

        for frame_number, r in enumerate(self.model.predict(
            video_path,
            conf=0.5,
            save=True,
            stream=True,
            # imgsz=(height, width),
        )):
            print(len(r.boxes.xywh))
            if len(r.boxes.xywh) > 0:
                if not last_frame_success:
                    start_timing = self.get_timing(fps, frame_number)
                    intervals[start_timing] = ''
                end_timing = self.get_timing(fps, frame_number)
                last_frame_success = True
            else:
                if last_frame_success:
                    intervals[start_timing] = end_timing
                last_frame_success = False

        if last_frame_success:
            intervals[start_timing] = end_timing

        return self.merge_intervals(intervals)

    def get_timing(self, fps, frame_number):
        frame_time = frame_number / fps
        hours = int(frame_time // 3600)
        minutes = int((frame_time % 3600) // 60)
        seconds = int(frame_time % 60)
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return formatted_time

    def get_video_info(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        return fps

    def merge_intervals(self, data):
        def str_to_time(time_str):
            return datetime.strptime(time_str, "%H:%M:%S")

        def time_to_str(time_obj):
            return time_obj.strftime("%H:%M:%S")

        intervals = [
            (str_to_time(start), str_to_time(end))
            for start, end in data.items()]
        intervals.sort()

        merged_intervals = []
        for start, end in intervals:
            if not merged_intervals:
                merged_intervals.append((start, end))
            else:
                last_start, last_end = merged_intervals[-1]
                if last_end < start - timedelta(seconds=1):
                    merged_intervals.append((start, end))
                else:
                    merged_intervals[-1] = (last_start, max(last_end, end))

        result = {
            time_to_str(start):
            time_to_str(end) for start, end in merged_intervals
        }
        return result
