from pydantic import BaseModel, HttpUrl
from typing import List


class PredictedPhotoData(BaseModel):
    link: str
    txt_path: str


class PredictPhotosResponse(BaseModel):
    predicted_data: List[PredictedPhotoData]
    type: str = "images"


class PredictVideoResponse(BaseModel):
    link: str
    marks: list[float]
    type: str = "video"


class VideoURL(BaseModel):
    url: HttpUrl
