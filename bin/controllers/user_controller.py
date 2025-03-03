import traceback
from urllib.parse import urljoin
import uuid
from fastapi import HTTPException
import base64
import re
import os
from mimetypes import guess_extension
from bin.response.response_model import ResponseModel,ErrorResponseModel,FalseResponseModel
from bin.services.api_service.hash_password import hash_password,verify_password
from bin.services.db_service.user_service import create_new_user,validate_user,add_record_to_favorite_list,get_food_list,insert_user_dietary_goal,update_user_dietary_values,get_user_dieatary_limit
from bin.services.jwt_auth import create_token
from fastapi.security import HTTPAuthorizationCredentials
from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session
from bin.models import pg_models

current_dir = os.path.join(os.getcwd(), 'public', 'images', 'avatars')
os.makedirs(current_dir, exist_ok=True)
http_base = os.getenv("APP_URL")
avatar_path = os.getenv("AVATAR_PATH")

db: Session = next(db_connection())

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
        
    def update_user_img(self,request, auth: HTTPAuthorizationCredentials):
        try:
            user = db.query(pg_models.User).get(auth.sub)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            img_b64 = request.base64_image.split("base64,", 1)[1]
            img_file = base64.b64decode(img_b64)
            img_mime = re.search(r'data:(.*);', request.base64_image).group(1)
            img_ext = guess_extension(img_mime) or ".jpg"  

            # Remove old image if exists
            if user.user_img:
                old_img_path = os.path.join(current_dir, os.path.basename(user.user_img))
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)

            # Generate a new unique filename
            filename = f"{uuid.uuid4().hex[:20].upper()}{img_ext}"
            file_path = os.path.join(current_dir, filename)

            # Save the new image
            with open(file_path, "wb") as binary_file:
                binary_file.write(img_file)

            # Update user record
            user.user_img = f"{filename}"  
            db.commit()
            db.refresh(user)

 
            return {
                "status": True,
                "result": "Image updated successfully",
                "img": f"{avatar_path}/{filename}" 
            }

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=400,
                detail={
                    "status": False,
                    "result": str(e)
                })

    def get_user_img(self,auth: HTTPAuthorizationCredentials):
        try:
            user = db.query(pg_models.User).get(auth.sub)

            return {
                "status": True,
                "result": f"{avatar_path}/{user.user_img}" if user.user_img else user.user_img
            }

        except Exception as e:
            raise HTTPException(
                status_code=200,
                detail={
                    "status": True,
                    "result": str(e)
                })

userManager = UserManager()