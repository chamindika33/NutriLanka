from bin.db.postgresDB import db_connection
from fastapi import HTTPException
from collections import OrderedDict
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import delete,update
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel

db: Session = next(db_connection())

def get_all_users(offset,record_per_page):
    try:
        data = db.query(
            pg_models.User
        ).filter(
            pg_models.User.role_id == 2
        ).order_by(pg_models.User.id.asc())
        data = data.offset(offset).limit(record_per_page).all()

        total_records = db.query(pg_models.User).count()

        result = {
            "total_records": total_records,
            "data": data
        }

        return result


    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)
    
def get_all_users_dietary_list(offset,record_per_page):
    try:
        data = db.query(
            pg_models.UserDietaryGoal
        ).order_by(pg_models.UserDietaryGoal.gole_id.asc())
        data = data.offset(offset).limit(record_per_page).all()

        total_records = db.query(pg_models.UserDietaryGoal).count()

        result = {
            "total_records": total_records,
            "data": data
        }

        return result


    except SQLAlchemyError as e:
        db.rollback()
        return ErrorResponseModel(str(e), 404)