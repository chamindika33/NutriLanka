from fastapi import FastAPI,APIRouter,Query
from fastapi.exceptions import HTTPException
from bin.requests.food_request import NewFoodRecord,FoodFilter
from bin.controllers.food_nutrition_controller import nutritionController

router = APIRouter(
    prefix="/nutri-lanka",
    tags=["Food"]
)

@router.post("/add-food-record")
def create_new_food_record(request:NewFoodRecord):
    return nutritionController.create_food_records(request)


@router.get("/get-food-nutrition-info")
def get_food_nutrition_info(size:float,name:str):
    return nutritionController.get_food_nutrition_info(size,name)

@router.post("/filter-food-record")
def filter_food_record(request:FoodFilter):
    return nutritionController.filter_food(request)
