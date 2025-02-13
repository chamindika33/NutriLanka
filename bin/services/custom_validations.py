import re
from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session
from sqlalchemy import delete,update,exists,and_
from bin.models import pg_models
from sqlalchemy.exc import SQLAlchemyError
from bin.response.response_model import ErrorResponseModel

db: Session = next(db_connection())

async def check_user_email(email):
   
    query = db.query(exists().where(
            and_(
                pg_models.User.email == email,
                pg_models.User.status == True 
            )
        )).scalar()
    
    return query

def email_validation(cls, value):
    if value == "":
        raise ValueError('email address required')

    pattern = "^[a-zA-Z0-9-._]+@[a-zA-Z0-9.]+\.[a-z]{1,3}$"
    if re.match(pattern, value):
        return value
    raise ValueError('Invalid email address')
