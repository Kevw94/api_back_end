import datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MessageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    senderId: Optional[PyObjectId] = Field(...)
    receiverId: Optional[PyObjectId] = Field(...)
    message: Optional[str]  # optional content if post = ""
    created_at: Optional[datetime.datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "Ceci est un exemple de content",
                "created_at": "2022-10-12T11:08:54.712000"
            }
        }


class GetMessageModel(BaseModel):
    message: Optional[str]  # optional content if post = ""
    created_at: Optional[datetime.datetime] = None
