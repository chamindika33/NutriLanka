import base64
import os
import json
from bin.response.response_model import ErrorResponseModel,FalseResponseModel, ResponseModel
from bin.services.db_service.food_service import create_new_food_record,get_food_info,get_filter_data,get_all_food_info,delete_records,insert_food_measurements,get_food_measurement_details,get_all_food_measurement,get_all_food_measurements_for_food,delete_food_measurements_for_food,update_existing_food_record,create_new_food_record2,get_food_ingredient_info

avatar_path = os.getenv("AVATAR_PATH")

class NutritionController():
    def create_food_records(self, request):
        try:
            print('type of image -',type(request.food_img))
            # Validate and parse the base64 data
            if not request.food_img or not isinstance(request.food_img, str):
                raise ValueError("Invalid or missing 'food_img' field in the request.")

            if "base64," not in request.food_img:
                raise ValueError("The 'food_img' field is not a valid base64-encoded image.")

            base64_data = request.food_img.split(",")[1] # Extract base64 image data after the comma

            image_data = base64.b64decode(base64_data) # Decode the base64 data

            file_dir = os.path.join(os.getcwd(), 'public', 'images', 'avatars')  # Absolute path to the images directory
            # Ensure the directory exists
            if not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)  # Create the directory if it doesn't exist

            img_name = f"{request.food_name}.jpg"  # Construct the image filename
            file_path = os.path.join(file_dir, img_name)  # Full file path 

            with open(file_path, "wb") as f:
                f.write(image_data)

            print(f"Image successfully saved at: {file_path}")
            print('request.ingredient',request.ingredient)
            ingredient_json = request.ingredient
            print('ingredient_json ',ingredient_json )
            create_new_food_record2(request,ingredient_json, img_name)
            return ResponseModel(request, "Successfully added food record")

        except (ValueError, base64.binascii.Error) as e:
            print(f"Invalid image data: {str(e)}")  # Handle specific decoding or format errors
            return ErrorResponseModel(str(e), 400)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e), 400)
        
    def add_food_measuremnts_to_food(self,request):
        try:
            insert_food_measurements(request)
            return ResponseModel(request, "Successfully enter food measuremnt")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e), 400)
        
    def get_food_nutrition_info(self, request):
        try:
            food_result = get_food_info(request.food_id)
            print('food result -->', food_result)

            if food_result:
                if hasattr(food_result, "__dict__"):
                    food_result = food_result.__dict__

                food_result = {k: v for k, v in food_result.items() if not k.startswith('_')}   

                if (food_result.get("food_img")) and (food_result.get("food_img") is not None):
                    image_url = food_result.get("food_img")
                    print('image url--->',image_url)
                    food_result["food_img"] = f"{avatar_path}/{image_url}"

                if request.unit_id == 7:
                    # Scale nutritional values based on size (default values are for 100g)
                    size = request.no_of_units
                  
                else:
                    data = get_food_measurement_details(request.food_id,request.unit_id)
                    size = data.weight_in_grams * request.no_of_units

                if request.no_of_units > 0:
                    scale_factor = size / 100
                    for key, value in food_result.items():
                        if isinstance(value, (float, int)):  # Only scale numerical values
                            food_result[key] = round(value * scale_factor, 2)

                return ResponseModel(food_result, "Successfully retrieved the data")
            
            else:
                return ResponseModel(food_result, "No data found")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e), 400)

        
    def filter_food(self,request):

        if request.filter_by == 'food':
            data = get_filter_data(request.filter_by,request.filter_pass,request.filter_name)
            fav_list = data['nutrition_data']
            print('result--->',fav_list)
            if not fav_list:
                return ResponseModel(data, "No nutrition data found.")

            # fav = fav_list[0] 
            food_info = [
                {
                    **fav,
                    "food_img": f"{avatar_path}/{fav['food_img']}"
                }
                for fav in fav_list
            ]
            # print('favvvv--->',fav)
            # if hasattr(fav,"__dict__"):
            #     print('hiiii')
            #     fav_dict = fav.__dict__.copy()
            #     fav_dict['food_img'] = f"{avatar_path}/{fav.food_img}" if hasattr(fav, "food_img") else None
            #     data["nutrition_data"] = fav_dict
            response_data = {
                "nutrition_data": food_info, 
                "measurement_data": data.get("measurement_data", [])  
            }
            return ResponseModel(response_data,"reterived data")
        
        else:
            data = get_filter_data(request.filter_by,request.filter_pass,request.filter_name)
            print('result--->',data)
            if not data:
                return ResponseModel(data, "No nutrition data found.")

            food_info = [
                {
                    **fav.__dict__,
                    "food_img": f"{avatar_path}/{fav.food_img}"
                }
                for fav in data
            ]
            
            return ResponseModel(food_info,"reterived data")

        
    def get_all_food_details(self,request):
        try:
            offset = (request.page_number-1) * request.record_per_page
            print('offset-->', offset)
            data = get_all_food_info(offset,request.record_per_page)
            food_info = [
                {
                    **fav.__dict__,
                    "food_img": f"{avatar_path}/{fav.food_img}"
                }
                for fav in data['data']
            ]
            result ={
                'data': food_info,
                'page_number': request.page_number,
                'record_per_page': request.record_per_page,
                'No of records': data['total_records']
            }

            return ResponseModel(result, "retrieved data")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def delete_food_records(self,request):
        try:
            delete_records(request.food_id)
            return ResponseModel(request.food_id, "deleted food record")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)


    def get_food_nutrition_list(self):
        try:
            nutrition_list = [
               'calories',
               'protein',
               'carbohydrates',
               'water',
               'fat',
               'vitamins',
               'fiber',
               'calcium',
               'magnesium',
               'phosphorus',
               'sodium',
               'potassium',
               'iron',
               'zinc',
               'selenium',
               'copper',
               'manganese'
           ]

            return ResponseModel(nutrition_list, "get all nutrition list")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def get_measurement_list(self):
        try:
            result = get_all_food_measurement()
            return ResponseModel(result, "get all food measurement list")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def get_specific_food_measurements(self,food_id):
        try:
            result = get_all_food_measurements_for_food(food_id)
            print('result-->',result)
            food_list = [{
                    "unit": "g",
                    "unit_name": "grams",
                    "weight_in_grams": 100,
                    "unit_id": 7
                }]
            if result:
                for food_measurement, food_unit in result:
                    food_list.append({
                        "unit_id":food_unit.unit_id,
                        "unit": food_unit.unit,
                        "unit_name": food_unit.unit_name,
                        "weight_in_grams": food_measurement.weight_in_grams

                    })
            return ResponseModel(food_list, "get all food measurements")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def delete_food_measurements(self,food_id,unit_id):
        try:
            result = delete_food_measurements_for_food(food_id,unit_id)
            return ResponseModel(result, "delete food measurements")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        

    def update_existing_food(self, request,food_id):
        try:
            print('type of image -',type(request.food_img))
            # Validate and parse the base64 data
            if not request.food_img or not isinstance(request.food_img, str):
                raise ValueError("Invalid or missing 'food_img' field in the request.")

            if "base64," not in request.food_img:
                raise ValueError("The 'food_img' field is not a valid base64-encoded image.")

            base64_data = request.food_img.split(",")[1] # Extract base64 image data after the comma

            image_data = base64.b64decode(base64_data) # Decode the base64 data

            file_dir = os.path.join(os.getcwd(), 'public', 'images', 'avatars')  # Absolute path to the images directory
            # Ensure the directory exists
            if not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)  # Create the directory if it doesn't exist

            img_name = f"{request.food_name}.jpg"  # Construct the image filename
            file_path = os.path.join(file_dir, img_name)  # Full file path 

            with open(file_path, "wb") as f:
                f.write(image_data)

            print(f"Image successfully saved at: {file_path}")
            update_existing_food_record(request, img_name,food_id)
            return ResponseModel(request, "Successfully added food record")

        except (ValueError, base64.binascii.Error) as e:
            print(f"Invalid image data: {str(e)}")  # Handle specific decoding or format errors
            return ErrorResponseModel(str(e), 400)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e), 400)
        
    def ingredient_list(self,request):
        try:
            food_result = get_food_info(request.food_id)
            print('food result -->', food_result)

            if food_result:
                if hasattr(food_result, "__dict__"):
                    food_result = food_result.__dict__

                food_result = {k: v for k, v in food_result.items() if not k.startswith('_')}   

                if (food_result.get("food_img")) and (food_result.get("food_img") is not None):
                    image_url = food_result.get("food_img")
                    print('image url--->',image_url)
                    food_result["food_img"] = f"{avatar_path}/{image_url}"

                if request.unit_id == 7:
                    # Scale nutritional values based on size (default values are for 100g)
                    size = request.no_of_units
                  
                else:
                    data = get_food_measurement_details(request.food_id,request.unit_id)
                    size = data.weight_in_grams * request.no_of_units

                if request.no_of_units > 0:
                    scale_factor = size / 100
                    ingredients = food_result.get("ingredients", [])
                    for ing in ingredients:
                        if isinstance(ing, dict) and "grams" in ing:
                            original_grams = ing["grams"]
                            ing["grams"] = round(original_grams * scale_factor, 2)

                    food_result["ingredients"] = ingredients
                
                food_result = {
                        "food_name": food_result.get("food_name"),
                        "food_img": food_result.get("food_img"),
                        "ingredients": food_result.get("ingredients")
                    }

                return ResponseModel(food_result, "Successfully retrieved the data")
            
            else:
                return ResponseModel(food_result, "No data found")


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e), 400)
        
nutritionController = NutritionController()