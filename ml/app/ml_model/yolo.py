# from ultralytics import YOLO

class YoloModel:
    # def __init__(self, model_path):
    #     self.model = YOLO(model_path)

    # def predict(self, img):
    #     return self.model.predict(img, conf=0.5)

    def __init__(self, model_path):
        pass

    def predict(
        self,
        media: str
    ):
        """
        Выдает путь к файлу с разметкой и пример разметки

        :param media: path to media
        :type media: str
        :return: (txt_path, txt_example)
        :rtype: (str, str)
        """
        txt_path = './yolov8/runs/detect/exp/labels'
        txt_example = '0 0.5 0.5 0.2 0.4'
        return txt_path, None
