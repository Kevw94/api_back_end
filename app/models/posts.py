import datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


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


class PostModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId = Field(...)
    content: str = Field(...)
    created_at: datetime.datetime = None

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


class PatchModel(BaseModel):
    content: str
