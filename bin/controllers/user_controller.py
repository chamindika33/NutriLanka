from fastapi import HTTPException
from bin.response.response_model import ResponseModel,ErrorResponseModel,FalseResponseModel
from bin.services.api_service.hash_password import hash_password,verify_password
from bin.services.db_service.user_service import create_new_user,validate_user,add_record_to_favorite_list,get_food_list,insert_user_dietary_goal,update_user_dietary_values,get_user_dieatary_limit
from bin.services.jwt_auth import create_token

class UserManager():
    async def create_user(self,request):
        try:

            bmi_value = round(request.weight / ((request.height / 100) ** 2), 2)

            user = {
                "user_name" : request.user_name,
                "email" :  request.email,
                "password" : hash_password(request.password),
                "date_of_birth" : request.date_of_birth,
                "gender" : request.gender,
                "location" : request.location,
                "height" : request.height,
                "weight" : request.weight,
                "bmi_value" : bmi_value,
                "email_verified" : True,
                "status" : True,
                "dietary_preferences" : request.dieatary_preferences,
                "role_id" : request.role_id

            }
                    
            await create_new_user(user)
            return ResponseModel(request, "Successfully create new user")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)

    def sign_in(self,request):
        try:
            user = validate_user(request.username)
            print('user-->',user)
        
            if user:
                if verify_password(pw=request.password, hash_pw=user.password):
                    
                    return {
                        "result": {
                            "id": user.id,
                            "name": user.name,
                            "user_img": user.user_img,
                            "email_address": user.email,
                            "date_of_birth": user.date_of_birth,
                            "gender": user.gender,
                            "location": user.location,
                            "height": user.height,
                            "weight": user.weight,
                            "bmi_value": user.bmi_value

                        },
                        "token": create_token(user=user)
                    }
                
                else:
                    raise HTTPException(401, {
                        "status": False,
                        "result": "Username or Password Incorrect"
                    })

            raise HTTPException(404, {
                "status": False,
                "result": "No registered user found. Please sign up"
            })

        except Exception as e:
            raise e
        
    
    def add_food_record_to_favorite_list(self,request,authentication):
        try:
            for food_id in request.food_ids:
                add_record_to_favorite_list(request.user_id,food_id)

            return ResponseModel(request,"Add food record to the user profile")
        
        except Exception as e:
            raise e
        
    def get_user_favourite_food_list(self,user_id,authentication):
        try:

            food_list = get_food_list(user_id)
            print('food list-->',food_list)
            fav_list = [
                    {
                        "food_id": fav.food.food_id,
                        "food_name": fav.food.food_name,
                        "calories": fav.food.calories,
                        "description": fav.food.description,
                        "food_img": fav.food.food_img
                    }
                    for fav in food_list
                ]

            return ResponseModel(fav_list, "Favorite food records retrieved successfully.")
        
        except Exception as e:
            raise e
        
    def set_user_dietary_goal(self,request,authentication):
        try:
            insert_user_dietary_goal(request)

            return ResponseModel(request, "Successfully set the dietary goal")
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def update_user_daily_limit(self,request,authentication):
        try:
            update_user_dietary_values(request)

            return ResponseModel(request, "update user dietary goal")


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        
    def get_user_daily_dieatary_limit(self,user_id,authentication):
        try:
            result = get_user_dieatary_limit(user_id)
            print(result)
            if result:
                def safe_float(value):
                    print(value)
                    if value == None:
                        return 0
                    return float(value)
                
                total_burn_value =  safe_float(result.breakfast_burn) + safe_float(result.lunch_burn) + safe_float(result.dinner_burn) + safe_float(result.intermediate_burn)
                                    
                result_dict = {
                    column.name: (getattr(result, column.name) if getattr(result, column.name) is not None else 0)
                    for column in result.__table__.columns
                }

                print(result_dict)
                result_dict['total_burn_value'] = total_burn_value        
                result_dict['target_value'] = result.target_value
                remain_value = abs(total_burn_value - result_dict['target_value'])

                result_dict['remaining_values'] = remain_value
                if remain_value == 0 :
                    result_dict['achievements'] = 'Goal Achieved'
                elif remain_value > 0 :
                    result_dict['achievements'] = 'Under Achieved'
                else:
                    result_dict['achievements'] = 'Over Achieved'

                return ResponseModel(result_dict, "get user daily dietary goal")
            else:
                return ErrorResponseModel('No data found',404)


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)


userManager = UserManager()