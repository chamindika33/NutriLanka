from sqlite3.dbapi2 import Timestamp
import uuid
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy import JSON, TEXT, Column, DateTime, String, Date, Numeric, func , Integer,Float,Boolean
from bin.db.postgresDB import Base,engine
from sqlalchemy.orm import column_property
from bin.services.generator import public_token


class Timestamp:
    created_at = Column(DateTime, default=func.now())  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) 

class User(Base,Timestamp):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    password = deferred(Column(TEXT, nullable=False))  # Deferred for security
    email = Column(TEXT, unique=True, nullable=False)
    user_img = Column(TEXT, nullable=True)  # Optional profile image
    age = Column(Integer, nullable=True)
    gender = Column(String(15), nullable=True)
    location = Column(String(255), nullable=True)
    height = Column(Integer, nullable=False)  # In cm
    weight = Column(Integer, nullable=False)  # In kg
    bmi_value = Column(Float, nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False)  # Set default to False
    dietary_preferences = Column(String(255), nullable=True)  
    status = Column(Boolean, nullable=False, default=True)  # Active status by default

class NutritionInfo(Base):
    __tablename__ = 'nutrition_info'

    food_id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String, index=True)
    native_name = Column(String, index=True)
    description = Column(String, index=True)
    calories = Column(Float, index=True)
    protein = Column(Float, index=True)
    carbohydrates= Column(Float, index=True)
    water= Column(Float, index=True)
    fat= Column(Float, index=True)
    vitamins= Column(Float, index=True)
    fiber= Column(Float, index=True)
    calcium= Column(Float, index=True)
    magnesium= Column(Float, index=True)
    phosphorus= Column(Float, index=True)
    sodium= Column(Float, index=True)
    potassium= Column(Float, index=True)
    iron= Column(Float, index=True)
    zinc= Column(Float, index=True)
    selenium= Column(Float, index=True)
    copper= Column(Float, index=True)
    manganese= Column(Float, index=True)
    food_img = Column(String, index=True)

class UserFavoriteFoodInfo(Base):
    __tablename__ = 'user_favorite_food'

    record_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    food_id = Column(Integer, ForeignKey('nutrition_info.food_id'))  
    
    food = relationship("NutritionInfo", backref="favorite_foods")
   
   
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")