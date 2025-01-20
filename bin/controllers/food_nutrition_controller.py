from bin.response.response_model import ErrorResponseModel,FalseResponseModel, ResponseModel
from bin.services.db_service.food_service import create_new_food_record,get_food_info,get_filter_data

class NutritionController():
    def create_food_records(self,request):
        try:
            create_new_food_record(request)
            return ResponseModel(request,"successfully added food record")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def get_food_nutrition_info(self,size,name):
        try:
            food_result =  get_food_info(name)
            
            if food_result:
                if hasattr(food_result,"__dict__"):
                    food_result = food_result.__dict__
                    food_result = {k: v for k, v in food_result.items() if not k.startswith('_')}

                    print('food result -->',food_result)

                if size and size>0:
                    scale_factor = size/100
                    for key,value in food_result.items():
                        if isinstance(value,(float)):
                            food_result[key] = round(value*scale_factor,2)
                            
                return ResponseModel(food_result,"succesfuly retirieved the data")
            else:
                return ResponseModel(food_result,"no data found")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)

    def filter_food(self,request):
        try:
            result = get_filter_data(request.filter_by,request.filter_pass,request.filter_name)
            return ResponseModel(result,"reterived data")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)


    


nutritionController = NutritionController()