from fastapi import FastAPI,APIRouter,Query
from fastapi.exceptions import HTTPException
from bin.requests.food_request import NewFoodRecord,FoodFilter,AllFoodData,DeleteFoodData,FoodMeasurements,FoodMeasurementsFilter,UpdateFoodRecord
from bin.controllers.food_nutrition_controller import nutritionController

router = APIRouter(
    prefix="/nutri-lanka",
    tags=["Food"]
)

@router.post("/add-food-record")
def create_new_food_record(request:NewFoodRecord):
    print('type of image -',type(request.food_img))
    return nutritionController.create_food_records(request)

@router.post("/add-food-measurements")
def add_food_measurement(request:FoodMeasurements):
   return nutritionController.add_food_measuremnts_to_food(request)
    

@router.post("/get-food-nutrition-info")
def get_food_nutrition_info(request:FoodMeasurementsFilter):
    return nutritionController.get_food_nutrition_info(request)


@router.post("/filter-food-record")
def filter_food_record(request:FoodFilter):
    return nutritionController.filter_food(request)

@router.post("/all-food-records")
def get_all_food_records(request:AllFoodData):
    return nutritionController.get_all_food_details(request)

@router.delete("/remove-food-records")
def remove_food_records(request:DeleteFoodData):
    return nutritionController.delete_food_records(request)

@router.get("/get-nutrition-list")
def get_nutrition_list():
    return nutritionController.get_food_nutrition_list()

@router.get("/get-food-measurement-list")
def get_food_measurement_list():
    return nutritionController.get_measurement_list()

@router.get("/get-food-measurement-details")
def get_food_measurement_details(food_id : int):
    return nutritionController.get_specific_food_measurements(food_id)

@router.put("/delete-food-measurement")
def delete_specific_food_measurement(food_id : int, unit_id :int):
    return nutritionController.delete_food_measurements(food_id,unit_id)

@router.put("/update-food-record/{food_id}")
def update_food_record(request:NewFoodRecord,food_id):
    print('type of image -',type(request.food_img))
    return nutritionController.update_existing_food(request,food_id)

@router.post("/get-ingredient-list")
def get_ingredient_list(request:FoodMeasurementsFilter):
    return nutritionController.ingredient_list(request)