import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from app.models.users import UserModel
from app.core.config import config


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
    message: str = Field(...)
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    user: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "message": "Hello World",
                "user": "Jane Doe",
            }
        }
