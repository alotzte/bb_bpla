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
            imgsz=(height, width),
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

        self.save_txt(txt_path, res)

        photo_url = upload_file_to_s3(link, 'bb-bpla', 'upd_photos')
        txt_url = upload_file_to_s3(txt_path, 'bb-bpla', 'upd_txts')
        # TODO: удалить файлы

        return {
            'link': photo_url,
            'txt_path': txt_url,
            # 'confidence':
        }

    def save_txt(self, path, result):
        with open(path, '+w') as file:
            for idx, prediction in enumerate(result[0].boxes.xywhn):
                cls = int(result[0].boxes.cls[idx].item())
                # Write line to file in YOLO label format : cls x y w h
                file.write(f"{cls} {prediction[0].item()} {prediction[1].item()} {prediction[2].item()} {prediction[3].item()}\n")
    
    # def predict_video(self, video_path):
    #     last_frame_success = False
    #     fps = self.get_video_info(video_path)
    #     intervals = {}

    #     for frame_number, r in enumerate(self.model.predict(
    #         video_path,
    #         conf=0.5,
    #         save=True,
    #         stream=True,
    #         # imgsz=(height, width),
    #     )):
    #         print(len(r.boxes.xywh))
    #         if len(r.boxes.xywh) > 0:
    #             if not last_frame_success:
    #                 start_timing = self.get_timing(fps, frame_number)
    #                 intervals[start_timing] = ''
    #             end_timing = self.get_timing(fps, frame_number)
    #             last_frame_success = True
    #         else:
    #             if last_frame_success:
    #                 intervals[start_timing] = end_timing
    #             last_frame_success = False

    #     if last_frame_success:
    #         intervals[start_timing] = end_timing

    #     return self.merge_intervals(intervals)

    # def get_timing(self, fps, frame_number):
    #     frame_time = frame_number / fps
    #     hours = int(frame_time // 3600)
    #     minutes = int((frame_time % 3600) // 60)
    #     seconds = int(frame_time % 60)
    #     formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    #     return formatted_time

    def get_video_info(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return fps, height, width, frames

    # def merge_intervals(self, data):
    #     def str_to_time(time_str):
    #         return datetime.strptime(time_str, "%H:%M:%S")

    #     def time_to_str(time_obj):
    #         return time_obj.strftime("%H:%M:%S")

    #     intervals = [
    #         (str_to_time(start), str_to_time(end))
    #         for start, end in data.items()]
    #     intervals.sort()

    #     merged_intervals = []
    #     for start, end in intervals:
    #         if not merged_intervals:
    #             merged_intervals.append((start, end))
    #         else:
    #             last_start, last_end = merged_intervals[-1]
    #             if last_end < start - timedelta(seconds=1):
    #                 merged_intervals.append((start, end))
    #             else:
    #                merged_intervals[-1] = (last_start, max(last_end, end))

    #     result = {
    #         time_to_str(start):
    #         time_to_str(end) for start, end in merged_intervals
    #     }
    #     return result

    def predict_video(self, video_path):
        fps, height, width, frames = self.get_video_info(video_path)
        object_name = os.path.basename(video_path)
        object_name, suffix = os.path.splitext(object_name)
        max_missed_frames = int(fps / 2)
        last_frame_success = False
        timestamps = []
        missed_frames = 0

        for frame_number, r in enumerate(self.model.predict(
            video_path,
            conf=0.5,
            save=True,
            stream=True,
            imgsz=(height, width),
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

        return video_url, timestamps
