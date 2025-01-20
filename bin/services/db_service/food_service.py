from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session
from sqlalchemy import delete,update
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel

db: Session = next(db_connection())

def create_new_food_record(request):
    try:
        data = pg_models.NutritionInfo(
            food_name = request.food_name,
            native_name = request.native_name,
            description = request.description,
            calories = request.calories,
            protein = request.protein,
            carbohydrates= request.carbohydrates,
            water= request.water,
            fat= request.fats,
            vitamins= request.vitamins,
            fiber = request.fiber,
            calcium = request.calcium,
            magnesium = request.magnesium,
            phosphorus = request.phosphorus,
            sodium = request.sodium,
            potassium = request.potassium,
            iron = request. iron,
            zinc = request.zinc,
            selenium = request.selenium,
            copper = request.copper,
            manganese = request.manganese
        )

        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorResponseModel(str(e), 404)
    
def get_food_info(name):
    try:
        data = db.query(
            pg_models.NutritionInfo
        ).filter(
            pg_models.NutritionInfo.native_name == name
        ).first()

        return data
    except SQLAlchemyError as e:
        raise ErrorResponseModel(str(e), 404)
    
def get_filter_data(filter_by,filter_pass,filter_name):
    try:
        if filter_by == 'food':
            data = db.query(
                    pg_models.NutritionInfo
                ).filter(
                    pg_models.NutritionInfo.native_name == filter_name
                ).first()
            
        elif filter_by == 'nutrition':
            ROW_LIMIT = 10
            colomn_to_filter = getattr(pg_models.NutritionInfo,filter_name,None)

            if colomn_to_filter is None:
                raise ValueError(f"Invalid filter name: {filter_name}")
            
            if filter_pass == 'high':
                data = (
                    db.query(pg_models.NutritionInfo)
                    .order_by(colomn_to_filter.desc())
                    .limit(ROW_LIMIT)
                    .all()
                )
            elif filter_pass == 'low':
                data = (
                    db.query(pg_models.NutritionInfo)
                    .order_by(colomn_to_filter.asc())
                    .limit(ROW_LIMIT)
                    .all()
                )
            else:
                raise ValueError(f"Invalid filter pass: {filter_pass}")

        else:
            raise ValueError(f"Invalid filter type: {filter_by}")
            
        return data

    except SQLAlchemyError as e:
        raise ErrorResponseModel(str(e), 404)