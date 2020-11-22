from pydantic import BaseModel
from typing import List 

class Payload(BaseModel):
    median_income_in_block: float
    median_house_age_in_block: int
    average_rooms: int
    average_bedrooms: int
    population_per_block: int
    average_house_occupancy: int
    block_latitude: float
    block_longitude: float

def payload_to_list(inputs: Payload) -> List :
	return [inputs.median_income_in_block,
			inputs.median_house_age_in_block,
			inputs.average_rooms,
			inputs.average_bedrooms,
			inputs.population_per_block,
			inputs.average_house_occupancy,
			inputs.block_latitude,
			inputs.block_longitude
			]