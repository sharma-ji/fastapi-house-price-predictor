from pydantic import BaseModel

class JWT_User(BaseModel):
	username : str
	password : str