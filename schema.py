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

