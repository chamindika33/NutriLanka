from bin.db.postgresDB import db_connection
from fastapi import HTTPException
from collections import OrderedDict
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import delete,update
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel

db: Session = next(db_connection())

def create_new_custom_food_record(request,image_data):
    try:
        data = pg_models.CustomRecipesInfo(
            food_name = request.food_name,
            description = request.description,
            weight = request. weight,
            food_measurement = request. food_measurements,
            calories = request.calories,
            protein = request.protein,
            carbohydrates= request.carbohydrates,
            water= request.water,
            fat= request.fat,
            vitamins= request.vitamins,
            fiber = request.fiber,
            calcium = request.calcium,
            sodium = request.sodium,
            iron = request. iron,
            potassium = request.potassium,
            food_img = image_data,
            user_id = request.user_id
        )

        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorResponseModel(str(e), 404)
    
def get_user_custom_food_list(user_id):
    try:
        data = db.query(pg_models.CustomRecipesInfo).filter(
                pg_models.CustomRecipesInfo.user_id== user_id
            ).all()
        
        print('data-->',data)
        
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    