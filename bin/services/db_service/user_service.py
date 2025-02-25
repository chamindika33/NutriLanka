from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import delete,update,exists,func
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel
from datetime import datetime, timezone

db: Session = next(db_connection())

    
async def create_new_user(user):
    try:
        print('--user--',user)
       
        data = pg_models.User(
            name = user["user_name"],
            password = user["password"],
            email = user["email"],
            date_of_birth = user["date_of_birth"],
            gender = user["gender"],
            location = user["location"],
            height = user["height"],
            weight = user["weight"],
            bmi_value = user["bmi_value"],
            email_verified = user["email_verified"],
            dietary_preferences = user["dietary_preferences"],
            status = user["status"],
            role_id = user["role_id"]
           
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    
def validate_user(email):
    try:
        data = db.query(
                pg_models.User
            ).filter(
                pg_models.User.email == email
            ).first()
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    
def add_record_to_favorite_list(user_id,food_id):
    try:
       
        data = pg_models.UserFavoriteFoodInfo(
                user_id = user_id,
                food_id = food_id
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)

def get_food_list(user_id):
    try:
        data = db.query(pg_models.UserFavoriteFoodInfo).options(
                joinedload(pg_models.UserFavoriteFoodInfo.food)
            ).filter(
                pg_models.UserFavoriteFoodInfo.user_id == user_id
            ).all()
        
        print('data-->',data)
        
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)

def insert_user_dietary_goal(request):
    try:
        data = pg_models.UserDietaryGoal(
                user_id = request.user_id,
                target_nutrient = request.target_nutrient,
                target_value = request.target_value

        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data


    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    
def update_user_dietary_values(request):
    try:
        today_date = datetime.now(timezone.utc).date()
        update_query = update(pg_models.UserDietaryGoal).where(
                        (pg_models.UserDietaryGoal.user_id == request.user_id) &
                        (func.date(pg_models.UserDietaryGoal.created_at) == today_date ) 
                    ).values(
                        breakfast_burn = request.breakfast,
                        lunch_burn = request.lunch,
                        dinner_burn = request.dinner,
                        intermediate_burn = request.intermediate

                    )
        result = db.execute(update_query)
        db.commit()

        rows_upadted = result.rowcount
        print("rows",rows_upadted)
        return rows_upadted

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    
def get_user_dieatary_limit(user_id):
    try:
        today_date = datetime.now(timezone.utc).date()
        data = db.query(pg_models.UserDietaryGoal).filter(
                (pg_models.UserDietaryGoal.user_id == user_id) &
                (func.date(pg_models.UserDietaryGoal.created_at) == today_date )
            ).first()
        
        print('data-->',data)
        
        return data

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)