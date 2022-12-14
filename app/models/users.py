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


class UserModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	username: str = Field(...)
	password: Optional[str]
	created_at: Optional[datetime.datetime]
	disabled: Optional[bool] | None = None

	

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"username": "Jane Doe",
				"password": "pass123",
			}
		}

class UserToFrontModel(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	username: str = Field(...)
	created_at: Optional[datetime.datetime]

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}
		schema_extra = {
			"example": {
				"id": "ObjectId(eazeazrzafs2332)",
				"username": "Jane Doe",
				"created_at": "date",
			}
		}
	
class ModifPasswordModel(BaseModel):
	current_password: str
	modified_password: str
