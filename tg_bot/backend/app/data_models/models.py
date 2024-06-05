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
