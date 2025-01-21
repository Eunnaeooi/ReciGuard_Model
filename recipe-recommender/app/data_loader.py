import pandas as pd
from sqlalchemy.orm import Session
from app.config import SessionLocal

# 데이터 로드 함수
def load_data(db: Session):
    Ingredient = pd.read_sql("SELECT * FROM ingredient", db.connection())
    Recipe_Ingredient = pd.read_sql("SELECT * FROM recipe_ingredient", db.connection())
    User_Ingredient = pd.read_sql("SELECT * FROM user_ingredient", db.connection())
    Recipe = pd.read_sql("SELECT * FROM recipe", db.connection())
    User_Cuisine = pd.read_sql("SELECT * FROM user_cuisine", db.connection())
    User_FoodType = pd.read_sql("SELECT * FROM user_foodtype", db.connection())
    User_CookingStyle = pd.read_sql("SELECT * FROM user_cookingstyle", db.connection())
    User_Scrap = pd.read_sql("SELECT * FROM user_scrap", db.connection())
    
    return Ingredient, Recipe_Ingredient, User_Ingredient, Recipe, User_Cuisine, User_FoodType, User_CookingStyle, User_Scrap
