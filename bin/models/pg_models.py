from sqlite3.dbapi2 import Timestamp
import uuid
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlalchemy import JSON, TEXT, Column, DateTime, String, Date, Numeric, func , Integer,Float,Boolean
from bin.db.postgresDB import Base,engine
from sqlalchemy.orm import column_property



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
    # age = Column(Integer, nullable=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(15), nullable=True)
    location = Column(String(255), nullable=True)
    height = Column(Integer, nullable=False)  # In cm
    weight = Column(Integer, nullable=False)  # In kg
    bmi_value = Column(Float, nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False)  # Set default to False
    dietary_preferences = Column(String(255), nullable=True)  
    status = Column(Boolean, nullable=False, default=True)  # Active status by default
    role_id = Column(Integer , ForeignKey("user_roles.id"), nullable=False)


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
   

class FoodUnit(Base):
    __tablename__ = 'food_unit'

    unit_id = Column(Integer, primary_key=True, index=True)
    unit = Column(String, index=True)
    unit_name = Column(String, index=True)
    unit_in_grams = Column(Float, index=True,nullable=True)

class FoodMeasurement(Base):
    __tablename__ = 'food_measurement'

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey('nutrition_info.food_id'), index=True)
    unit_id = Column(Integer, ForeignKey('food_unit.unit_id'), index=True)
    weight_in_grams = Column(Float, nullable=False)  # Defines how much 1 unit weighs in grams

    # Relationships
    food = relationship("NutritionInfo", back_populates="measurements")
    unit = relationship("FoodUnit", back_populates="measurements")

NutritionInfo.measurements = relationship("FoodMeasurement", back_populates="food", cascade="all, delete-orphan")
FoodUnit.measurements = relationship("FoodMeasurement", back_populates="unit", cascade="all, delete-orphan")

class UserRole(Timestamp, Base):
    __tablename__ = "user_roles"

    id = Column(Integer , primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)


   
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")