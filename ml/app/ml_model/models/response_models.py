from pydantic import BaseModel, HttpUrl
from typing import List


class PredictedPhotoData(BaseModel):
    link: str
    txt_path: str

class PredictedVideoData(BaseModel):
    link: str
    marks: list[float]


class PredictPhotosResponse(BaseModel):
    predicted_data: List[PredictedPhotoData]
    type: str = "images"


class PredictVideoResponse(BaseModel):
    predicted_data: List[PredictedVideoData]
    type: str = "video"


class VideoURL(BaseModel):
    url: HttpUrl
