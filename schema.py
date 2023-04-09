from pydantic import validator, BaseModel, EmailStr
from typing import Optional


class CreateUser(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @validator('password')
    def strong_password(cls, value):
        if len(value) < 8:
            raise ValueError('password too short')
        return value

class PatchUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    @validator('password')
    def strong_password(cls, value):
        if len(value) < 8:
            raise ValueError('password too short')
        return value

class CreateAdvertisement(BaseModel):

    title: str
    description: str
    email: EmailStr
    password: str

    @validator('title')
    def validate_title(cls, value):
        bad_word = ['Плохое слово1', 'Плохое слово2']
        if value in bad_word:
            raise ValueError('You add bads words')
        return value

class PatchAdvertisement(BaseModel):

    title: Optional[str]
    description: Optional[str]
    email: EmailStr
    password: Optional[str]

    @validator('title')
    def validate_title(cls, value):
        bad_word = ['Плохое слово1', 'Плохое слово2']
        if value in bad_word:
            raise ValueError('You add bads words')
        return value