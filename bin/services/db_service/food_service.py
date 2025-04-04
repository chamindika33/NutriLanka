from bin.db.postgresDB import db_connection
from fastapi import HTTPException
from collections import OrderedDict
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import delete,update,or_
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel

db: Session = next(db_connection())

def create_new_food_record(request,image_data):
    try:
        data = pg_models.NewNutritionInfo(
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
            manganese = request.manganese,
            food_img = image_data
            # ingredients =  ingredient_json

        )

        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorResponseModel(str(e), 404)
    
def create_new_food_record2(request,ingredient_json,image_data):
    try:
        data = pg_models.NewNutritionInfo(
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
            manganese = request.manganese,
            food_img = image_data,
            ingredients =  ingredient_json

        )

        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorResponseModel(str(e), 404)
    
def get_food_info(food_id):
    try:
        data = db.query(
            pg_models.NewNutritionInfo
        ).filter(
            pg_models.NewNutritionInfo.food_id == food_id
        ).first()

        return data
    except SQLAlchemyError as e:
        raise ErrorResponseModel(str(e), 404)
    
    
def get_filter_data(filter_by,filter_pass,filter_name):
    try:
        if filter_by == 'food':
            ROW_LIMIT = 10
            result = db.query(
                    pg_models.NewNutritionInfo
                ).filter(
                    or_(
                        pg_models.NewNutritionInfo.native_name.ilike(filter_name),
                        pg_models.NewNutritionInfo.native_name.ilike(f"{filter_name.lower()}%"),
                        pg_models.NewNutritionInfo.food_name.ilike(filter_name),
                        pg_models.NewNutritionInfo.food_name.ilike(f"{filter_name.lower()}%")
                    )
                    
                ).limit(ROW_LIMIT).all()
            
            if not result:
                raise HTTPException(status_code=404, detail="Nutrition data not found")
            
            food_ids = [food.food_id for food in result]
            result2= db.query(
                    pg_models.FoodMeasurement
                ).filter(
                    pg_models.FoodMeasurement.food_id.in_(food_ids)
                ).all()
            
            measurement_data = [{
                    "unit": "g",
                    "unit_name": "grams",
                    "unit_in_grams": 100,
                    "unit_id": 7
                }]
            if not result2:
                measurement_data
             
            else:
                unit_ids = {record.unit_id for record in result2}

                units = db.query(pg_models.FoodUnit).filter(
                        pg_models.FoodUnit.unit_id.in_(unit_ids)
                    ).all()

                unit_map = {
                    unit.unit_id: {
                        "unit": unit.unit_name,
                        "unit_name": unit.unit_name,
                        "unit_in_grams": unit.unit_in_grams,
                        "unit_id": unit.unit_id
                    } for unit in units
                }

                for record in result2:
                    measurement_data.append(unit_map.get(record.unit_id))  

            data = {
                "nutrition_data": [food.__dict__.copy() for food in result],
                "measurement_data": measurement_data
            }
        
        elif filter_by == 'nutrition':
            ROW_LIMIT = 10
            colomn_to_filter = getattr(pg_models.NewNutritionInfo,filter_name,None)

            if colomn_to_filter is None:
                raise ValueError(f"Invalid filter name: {filter_name}")
            
            if filter_pass == 'high':
                data = (
                    db.query(pg_models.NewNutritionInfo)
                    .order_by(colomn_to_filter.desc())
                    .limit(ROW_LIMIT)
                    .all()
                )
            elif filter_pass == 'low':
                data = (
                    db.query(pg_models.NewNutritionInfo)
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
    
def get_all_food_info(offset,record_per_page):
    try:
        data = db.query(
            pg_models.NewNutritionInfo
        ).order_by(pg_models.NewNutritionInfo.food_id.asc())
        data = data.offset(offset).limit(record_per_page).all()

        total_records = db.query(pg_models.NewNutritionInfo).count()

        result = {
            "total_records": total_records,
            "data": data
        }

        return result

    except SQLAlchemyError as e:
        raise ErrorResponseModel(str(e), 404)
    
def delete_records(food_id):
    try:
        delete_query = delete(pg_models.NewNutritionInfo).where(
            pg_models.NewNutritionInfo.food_id == food_id
        )

        result = db.execute(delete_query)
        db.commit()

        rows_deleted = result.rowcount
        return rows_deleted
    
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return 0
    
def insert_food_measurements(request):
    try:
        data = pg_models.FoodMeasurement(
           food_id = request.food_id,
           unit_id = request.unit_id,
           weight_in_grams =  request.weight_in_grams

        )

        db.add(data)
        db.commit()
        db.refresh(data)
        return data

    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorResponseModel(str(e), 404)
    
def get_food_measurement_details(food_id,unit_id):
    try:
        data= db.query(
                pg_models.FoodMeasurement
            ).filter(
              (pg_models.FoodMeasurement.food_id == food_id) and
              (pg_models.FoodMeasurement.unit_id == unit_id)
            ).first()

        return data
    
    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorResponseModel(str(e), 404)
    
def get_all_food_measurement():
    try:
        data = db.query(
            pg_models.FoodUnit
        ).order_by(pg_models.FoodUnit.unit_id.asc()).all()
  
        return data

    except SQLAlchemyError as e:
        raise ErrorResponseModel(str(e), 404)
    
def get_all_food_measurements_for_food(food_id):
    try:
        data = db.query(
            pg_models.FoodMeasurement,
            pg_models.FoodUnit
        ).filter(
            pg_models.FoodMeasurement.food_id == food_id
        ).join(
            pg_models.FoodUnit,
            (pg_models.FoodMeasurement.unit_id) == (pg_models.FoodUnit.unit_id)
        ).all()

        return data

    except SQLAlchemyError as e:
        raise ErrorResponseModel(str(e), 404)
    
def delete_food_measurements_for_food(food_id,unit_id):
    try:
        delete_query = delete(pg_models.FoodMeasurement).where(
            (pg_models.FoodMeasurement.food_id == food_id) &
            (pg_models.FoodMeasurement.unit_id == unit_id)
        )

        result = db.execute(delete_query)
        db.commit()

        rows_deleted = result.rowcount
        return rows_deleted
    
    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        return 0
    
def update_existing_food_record(request, img_name,food_id):
    try:
        update_query = update(pg_models.NewNutritionInfo).where(
                        (pg_models.NewNutritionInfo.food_id== food_id) 
                    ).values(
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
                        manganese = request.manganese,
                        food_img = img_name

                    )
        result = db.execute(update_query)
        db.commit()

        rows_upadted = result.rowcount
        print("rows",rows_upadted)
        return rows_upadted

    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    

def get_food_ingredient_info(food_id):
    try:
        data = db.query(
            pg_models.NewNutritionInfo.food_name.label("food_name"),
            pg_models.NewNutritionInfo.food_img.label("food_img"),
            pg_models.NewNutritionInfo.ingredients.label("ingredients")
        ).filter(
            pg_models.NewNutritionInfo.food_id == food_id
        ).limit(1).first()
        print('dataaaa--->',data)
        return data
    except SQLAlchemyError as e:
        db.rollback()  
        print("DB error:", str(e))
        raise HTTPException(status_code=400, detail=str(e))