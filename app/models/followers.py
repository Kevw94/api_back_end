import datetime
from typing import Optional
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


class FollowersModel(BaseModel):
	id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
	userId: Optional[PyObjectId] = Field(default_factory=PyObjectId)
	followingId: Optional[PyObjectId] = Field(default_factory=PyObjectId)
	created_at: Optional[datetime.datetime]

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"userId": "23432434223",
				"followingId": "354345345",
			}
		}


class FollowedModel(BaseModel):
	followingId: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"followingId": "354345345",
			}
		}
