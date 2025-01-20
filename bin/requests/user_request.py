from uuid import UUID
from pydantic import BaseModel,validator
from typing import List

class NewUser(BaseModel):
    name: str
    password: str
    email: str
    age:int
    gender:str
    location:int
    height:int
    weight:int
    dieatary_preferences:str
    
