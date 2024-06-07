from pydantic import BaseModel, HttpUrl
from typing import List


class PhotoResponse(BaseModel):
    link: str
    txt_path: str


class PredictPhotoResponse(BaseModel):
    data: List[PhotoResponse]
    type: str = "images"


class PredictVideoResponse(BaseModel):
    link: str
    marks: list[float]
    type: str = "video"


class VideoURL(BaseModel):
    url: HttpUrl
