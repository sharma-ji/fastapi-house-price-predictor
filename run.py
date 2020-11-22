from fastapi import FastAPI, HTTPException
from routes.v1 import app_v1
from utils.security import check_jwt_token,authenticate_user,create_jwt_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic_models.user import JWT_User
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI(title = 'House Price Predictor', version = "1.0.0")

app.include_router(app_v1, prefix = '/v1', dependencies = [Depends(check_jwt_token)])

@app.post('/token')
async def get_token_for_logging(form : OAuth2PasswordRequestForm = Depends()):
	jwt_dict = {'username' : form.username ,'password' : form.password }
	jwt_user = JWT_User(**jwt_dict)
	is_user = authenticate_user(jwt_user)
	if not is_user:
		raise HTTPException(status_code = HTTP_401_UNAUTHORIZED)
	jwt_token = create_jwt_token(jwt_user)
	return {'access_token' :jwt_token}

@app.middleware('http')
async def middleware(request : Request, call_next):
	if not any(word in str(request.url) for word in ["/token","/docs","redoc", "openapi.json"]):
		try:
			jwt_token = request.headers['Authorization'].split("Bearer ")[1]
			print(jwt_token)
			is_valid = check_jwt_token(jwt_token)
		except Exception as e:
			is_valid = False 
		if not is_valid:
			return Response('UnAuthorized', HTTP_401_UNAUTHORIZED)
	response = await call_next(request)
	return response
