import datetime
from pydantic import BaseModel, Field
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


class CommentsModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	postId: PyObjectId = Field(default_factory=PyObjectId)
	userId: Optional[PyObjectId]
	content: Optional[str] # optional content if comments = ""
	created_at: Optional[datetime.datetime] = None,

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"postId": "ObjectId(eazaze2134)",
				"userId": "ObjectId(eazazeezazea2134)",
				"content": "Ceci est un exemple de content",
				"created_at": "2022-10-12T11:08:54.712000"
			}
		}
