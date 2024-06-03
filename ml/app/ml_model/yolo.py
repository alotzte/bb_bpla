from ultralytics import YOLOv10


class YoloModel:
    def __init__(self, model_path):
        self.model = YOLOv10(model_path)

    def predict(self, img):
        res = self.model.predict(img, conf=0.5)
        try:
            return int(res[0].boxes.cls.to("cpu").tolist()[0]), res[0].boxes.xywh.to("cpu").tolist()[0]
        except:
            return None, None


    # def predict(
    #     self,
    #     media: str
    # ):
    #     """
    #     Выдает путь к файлу с разметкой и пример разметки

    #     :param media: path to media
    #     :type media: str
    #     :return: (txt_path, txt_example)
    #     :rtype: (str, str)
    #     """
    #     txt_path = './yolov8/runs/detect/exp/labels'
    #     txt_example = '0 0.5 0.5 0.2 0.4'
    #     return txt_path, txt_example
