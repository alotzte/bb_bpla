from uuid import UUID
from pydantic import BaseModel, HttpUrl
from typing import List


class PredictedPhotoData(BaseModel):
    link: str
    txt_path: str
    correlation_id: UUID


class PredictedVideoData(BaseModel):
    link: str
    marks: List[float]


class PredictPhotosResponse(BaseModel):
    predicted_data: List[PredictedPhotoData]
    type: str = "images"


class PredictVideoResponse(BaseModel):
    predicted_data: List[PredictedVideoData]
    type: str = "video"


class VideoURL(BaseModel):
    url: HttpUrl


class ArchiveURL(BaseModel):
    url: HttpUrl


class UrlsModel(BaseModel):
    urls: List[str]


class PhotosObject(BaseModel):
    url: str
    correlation_id: UUID


class UrlsModelPhoto(BaseModel):
    photos: List[PhotosObject]


class ArchiveObject(BaseModel):
    url: str
    correlation_id: UUID


class UrlsModelArchive(BaseModel):
    archives: List[ArchiveObject]