from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel,EmailStr, Field, field_validator
from typing import List, Any, Optional , Union
from bin.services.custom_validations import email_validation

class NewUser(BaseModel):
    user_name: str
    password: str
    email: EmailStr
    # age:int
    date_of_birth : date
    gender:str
    location:str
    height:int #should be in cm
    weight:int
    dieatary_preferences:str
    role_id: int
    


class UserLoginRequest(BaseModel):

    username: EmailStr
    password: str = Field(...)


    @field_validator('username')
    def func(cls, value):
        method = None
        if isinstance(value, str):
            method = 'email'
            email_validation(cls,value)

        if isinstance(value, type(None)):
            raise ValueError('Email required')
        
        setattr(cls , 'method' , method)
        return value
   

class AddFavoriteItem(BaseModel):
    user_id : str
    food_ids : List[int]

class SetDieatGoals(BaseModel):
    user_id : str
    target_nutrient : str
    target_value : float

class SetDailyLimit(BaseModel):
    user_id : str
    breakfast : float
    lunch : float
    dinner : float
    intermediate : float

class AvatarUpdateRequest(BaseModel):
    base64_image: str


class AddCustomRecipe(BaseModel):
    user_id : str
    food_name: str
    description: Optional[str]
    weight: float
    food_measurements: str
    calories : float
    protein : float
    carbohydrates: float
    water: float
    fat: float
    vitamins: float
    fiber: float
    calcium: float
    sodium: float
    iron: float
    potassium: float
    food_img: Optional[str] = None # Base64-encoded string
