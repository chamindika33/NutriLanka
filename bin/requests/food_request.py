from uuid import UUID
from pydantic import BaseModel,validator
from typing import List

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


class FoodFilter(BaseModel):
    filter_by: str #food/nutrition
    filter_pass: str # high/low
    filter_name: str #food name
    