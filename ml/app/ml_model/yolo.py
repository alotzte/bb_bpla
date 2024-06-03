import os
from ultralytics import YOLOv10

FULL_PATH_TO_TXT = '/app/ml_model/results/'


class YoloModel:
    def __init__(self, model_path):
        self.model = YOLOv10('/app/ml_model/weights/yolov10n.pt')
        # self.model = YOLOv10(model_path)

    def predict_photos(self, img, filename):
        width, height = img.size
        res = self.model.predict(
            img,
            conf=0.5,
            imgsz=(height, width),
        )  # TODO augment

        # TODO: создать папки
        name_img = f"""{
            os.path.join(
                FULL_PATH_TO_TXT, 'img', os.path.splitext(filename)[0])}.jpg"""

        name_txt = f"""{
            os.path.join(
                FULL_PATH_TO_TXT, 'txt', os.path.splitext(filename)[0])}.txt"""

        # TODO: Продумать куда сохранять
        res[0].save(name_img)
        res[0].save_txt(name_txt)
        # TODO: Проверить сохранение

        return {
            'path_to_photo_with_bbox': name_img,
            'path_to_txt': name_txt
        }

        # bbox_list = []
        # try:
        #     for r in res[0].boxes:
        #         box_cls, box_xywh = int(r.cls.to("cpu").tolist()[0]), \
        #             r.xywh.to("cpu").tolist()[0]
        #         bbox_list.append(self._generate_txt_string(box_cls, box_xywh))

        #     if len(bbox_list) > 0:
        #         return self._generate_txt_file_from_list(
        #             bbox_list,
        #             os.path.join(
        #                 FULL_PATH_TO_TXT,
        #                 os.path.splitext(filename)[0] + '.txt'
        #             )
        #         )
        #     else:
        #         return None
        # except:
        #     return None

    def _generate_txt_string(self, box_cls, box_xywh):
        return f'{box_cls} {" ".join(map(str, box_xywh))}'

    def _generate_txt_file_from_list(self, bbox_list, full_path):
        with open(full_path, 'w') as f:
            for bbox in bbox_list:
                f.write(bbox + '\n')

        return full_path
