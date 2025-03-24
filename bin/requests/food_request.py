from uuid import UUID
from pydantic import BaseModel,validator
from typing import List, Optional,Dict
import json

class NewFoodRecord(BaseModel):
    food_name: str
    native_name: str
    description: str
    calories : float
    protein : float
    carbohydrates: float
    water: float
    fats: float
    vitamins: float
    fiber: float
    calcium: float
    magnesium: float
    phosphorus: float
    sodium: float
    potassium: float
    iron: float
    zinc: float
    selenium: float
    copper: float
    manganese: float
    food_img: Optional[str] = None # Base64-encoded string
    ingredient: List[Dict]

    def get_parsed_ingredient(self) -> List[Dict]:
        return json.loads(self.ingredient)


class FoodFilter(BaseModel):
    filter_by: str #food/nutrition
    filter_pass: str # high/low
    filter_name: str #food name
    

class AllFoodData(BaseModel):
    page_number : int
    record_per_page : int

class DeleteFoodData(BaseModel):
   food_id : int

class FoodMeasurements(BaseModel):
   food_id : int
   unit_id : int
   weight_in_grams : float


class FoodMeasurementsFilter(BaseModel):
   food_id : int
   unit_id : int
   no_of_units : int


class UpdateFoodRecord(BaseModel):
    food_name: str
    native_name: str
    description: str
    calories : float
    protein : float
    carbohydrates: float
    water: float
    fats: float
    vitamins: float
    fiber: float
    calcium: float
    magnesium: float
    phosphorus: float
    sodium: float
    potassium: float
    iron: float
    zinc: float
    selenium: float
    copper: float
    manganese: float