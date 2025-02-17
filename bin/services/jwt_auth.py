import os
import jwt
from datetime import datetime, timezone, timedelta
from bin.db.postgresDB import db_connection
from sqlalchemy.orm import Session, joinedload
from bin.models.pg_models import UserRole

db: Session = next(db_connection())

exp = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))
algorithm = os.getenv('JWT_ALGORITHM')
key = os.getenv('JWT_SECRET_KEY')


def create_token(user):
    user_roles = db.query(UserRole.id).all()
    audiens = [role.id for role in user_roles]

    current_time = datetime.now(tz=timezone.utc)
    payload_data = {
        "iat": current_time,
        "nbf": current_time,
        "exp": current_time + timedelta(minutes=exp),
        "sub": str(user.id),
        "aud": audiens
    }

    token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm=algorithm
    )
    return token