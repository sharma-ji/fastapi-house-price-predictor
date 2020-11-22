import jwt 
from passlib.context import CryptContext
from pydantic_models.user import JWT_User
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY, USERNAME, PASSWORD
from datetime import datetime, timedelta
import time 
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth_schema = OAuth2PasswordBearer(tokenUrl= '/token')
pwd_context = CryptContext(schemes = ['bcrypt'])

def get_hashed_password(plain_text : str) ->str:
	return pwd_context.hash(plain_text)

def verify_password(plain_password : str, hashed_password : str):
	try:
		return pwd_context.verify(plain_password, hashed_password)
	except Exception as e:
		return False

def authenticate_user(user : JWT_User) ->bool:
	print('Auth--', user.username)
	print('Auth--', user.password)
	if user.username == USERNAME:
		if verify_password(user.password, PASSWORD):
			return True
	return False 

def create_jwt_token(user: JWT_User)->str:
	expiration = datetime.utcnow() + timedelta(minutes = JWT_EXPIRATION_TIME_MINUTES)
	jwt_payload = {'sub' : user.username,
					'exp': expiration}
	jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm = JWT_ALGORITHM)
	return jwt_token

def check_jwt_token(jwt_token: str = Depends(oauth_schema)):
	try: 
		jwt_payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithm = JWT_ALGORITHM)
		username = jwt_payload.get('sub')
		expiration = jwt_payload.get('exp')

		if time.time() < expiration:
			if username == USERNAME:
				return True 
	except Exception as e:
		return False 
	return False 