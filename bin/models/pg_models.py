from sqlite3.dbapi2 import Timestamp
import uuid
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON, TEXT, Column, DateTime, String, Date, Numeric, func , Integer,Float
from bin.db.postgresDB import Base,engine
from sqlalchemy.orm import column_property
from bin.services.generator import public_token

class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4() ,primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    password = deferred(Column(TEXT, nullable=False))
    email = Column(TEXT, unique=True , nullable=False)
    user_img = Column(TEXT)
    age = Column(Integer, nullable=False)
    gender = Column(String(15), nullable=True)
    location = Column(String(255), nullable=True)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    bmi_value = Column(Float, nullable=False)
    email_verified = Column(DateTime, nullable=True)
    dietary_preferences = Column(String(255), nullable=False) #Vegetarianism #Veganism #Kosher #Keto #Diabetes #Low carb
    status = deferred(Column(Numeric))
    # user_role = relationship("UserHasUserRoles" , back_populates="users" , lazy='dynamic')
    

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
   
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")