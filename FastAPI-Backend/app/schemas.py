from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    image: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    chatID: str
    message: str
    sender: str
    isFile: bool
    mimeType: Optional[str] = None
    filename: Optional[str] = None

class ImageSave(BaseModel):
    username: str
    image: str
    type: str
