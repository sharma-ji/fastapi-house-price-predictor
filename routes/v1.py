from pydantic_models.inputs import Payload
from pydantic_models.prediction import model_output
from fastapi import APIRouter
from services.model import HousePricePredictor
from utils.const import MODEL_PATH

app_v1 = APIRouter()

@app_v1.post('/predict', response_model = model_output, name = 'predict')
async def end_point_for_prediction(payload : Payload):
	model = HousePricePredictor(MODEL_PATH)
	prediction : model_output = model.predict(payload)
	return prediction 