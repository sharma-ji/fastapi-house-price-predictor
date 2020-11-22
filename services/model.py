from utils.const import MODEL_PATH, MULTIPLIER
import joblib
import numpy as np 
from pydantic_models.inputs import Payload, payload_to_list
from pydantic_models.prediction import model_output
from typing import List
import os
class HousePricePredictor(object):
	def __init__(self,path):
		print(os.getcwd()
		self.path = path 
		self._load_local_model()

	def _load_local_model(self):
		self.model = joblib.load(MODEL_PATH)

	def _pre_processing(self, features : Payload) -> np.ndarray:
		pre_processed = np.array(payload_to_list(features)).reshape(1,-1)
		return pre_processed

	def _post_processed(self, inputs: np.ndarray) -> List:
		result = inputs.tolist()
		result = result[0] * MULTIPLIER
		final_result = model_output(median_house_value = result)
		return final_result 

	def _predict(self, features : np.ndarray):
		predicted = self.model.predict(features)
		return predicted 
		
	def predict(self, payload: Payload):
		if payload is None:
			raise ValueError(f'{payload} is of Invalid Type')
		pre_processed = self._pre_processing(payload)
		predicted =  self._predict(pre_processed)
		post_prediction = self._post_processed(predicted)
		return post_prediction
