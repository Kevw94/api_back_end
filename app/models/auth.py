from pydantic import BaseModel
from bson.objectid import ObjectId
from datetime import datetime

class AuthModel(BaseModel):
	id: str | None = None
	username: str
	password: str
	created_at: datetime = None


	class Config:
		orm_mode = True
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders = {ObjectId: str}


