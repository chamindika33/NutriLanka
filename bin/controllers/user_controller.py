
from fastapi import HTTPException
from bin.response.response_model import ResponseModel,ErrorResponseModel
from bin.services.api_service.hash_password import hash_password,verify_password
from bin.services.db_service.user_service import create_new_user,validate_user,add_record_to_favorite_list,get_food_list,insert_user_dietary_goal
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
                "role_id" : 2

            }
                    
            await create_new_user(user)
            return ResponseModel(request, "Successfully create new user")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def sign_in(self,request):
        try:
            user = validate_user(request.username)
        
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
        
    
    def add_food_record_to_favorite_list(self,request):
        try:
            for food_id in request.food_ids:
                add_record_to_favorite_list(request.user_id,food_id)

            return ResponseModel(request,"Add food record to the user profile")
        
        except Exception as e:
            raise e
        
    def get_user_favourite_food_list(self,user_id):
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
        
    def set_user_dietary_goal(self,request):
        try:
            insert_user_dietary_goal(request)

            return ResponseModel(request, "Successfully set the dietary goal")
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return ErrorResponseModel(str(e),400)
        


userManager = UserManager()