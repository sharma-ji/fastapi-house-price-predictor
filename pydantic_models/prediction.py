from pydantic import BaseModel

class model_output(BaseModel):
	median_house_value: int
	currency : str = "$"
	