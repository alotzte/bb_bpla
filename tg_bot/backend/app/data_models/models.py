from typing import List
from pydantic import BaseModel


class UserRequest(BaseModel):
    user_id: int | str


class ObjectItem(BaseModel):
    id: int
    name: str
    checked: bool
    inputData: int


class UpdateObjectItem(BaseModel):
    id: int
    checked: bool
    inputData: int


class ObjectListResponse(BaseModel):
    objects: List[ObjectItem]


class UpdateObjectsRequest(BaseModel):
    user_id: str
    objects: List[UpdateObjectItem]


class Photos_data(BaseModel):
    classes: float
    confidence: float


class MLDataRequest(BaseModel):
    data: Photos_data


class MessageData(BaseModel):
    photo_url: str
    txt_url: str
    classes: List[float]
    confs: List[float]
