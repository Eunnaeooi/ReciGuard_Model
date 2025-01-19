import pandas as pd
from sqlalchemy import create_engine
import cryptography
from app.config import host, port, user, password, database, charset

# SQLAlchemy 엔진 생성
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
)

def load_data():
    
    Ingredient = pd.read_sql("SELECT * FROM ingredient", engine)
    Recipe_Ingredient = pd.read_sql("SELECT * FROM recipe_ingredient", engine)
    User_Ingredient = pd.read_sql("SELECT * FROM user_ingredient", engine)
    Recipe = pd.read_sql("SELECT * FROM recipe", engine)
    User_Cuisine = pd.read_sql_query("SELECT * FROM user_cuisine", engine)
    User_FoodType = pd.read_sql_query("SELECT * FROM user_foodtype", engine)
    User_CookingStyle = pd.read_sql_query("SELECT * FROM user_cookingstyle", engine)
    User_Scrap = pd.read_sql_query("SELECT * FROM user_scrap", engine)
    
    return Ingredient, Recipe_Ingredient, User_Ingredient, Recipe, User_Cuisine, User_FoodType, User_CookingStyle, User_Scrap


'''
import os

def load_data():
    
    DATA_PATH = "data/"
    
    INGREDIENT_PATH = os.path.join(DATA_PATH, "Ingredient.csv")
    RECIPE_INGREDIENT_PATH = os.path.join(DATA_PATH, "Recipe_Ingredient.csv")
    USER_INGREDIENT_PATH = os.path.join(DATA_PATH, "User_Ingredient.csv")
    Recipe_PATH = os.path.join(DATA_PATH, "Recipe.csv")
    User_Cuisine_PATH = os.path.join(DATA_PATH, "User_Cuisine.csv")
    User_FoodType_PATH = os.path.join(DATA_PATH, "User_FoodType.csv")
    User_CookingStyle_PATH = os.path.join(DATA_PATH, "User_CookingStyle.csv")
    User_Scrap_PATH = os.path.join(DATA_PATH, "User_Scrap.csv")

    Ingredient = pd.read_csv(INGREDIENT_PATH)
    Recipe_Ingredient = pd.read_csv(RECIPE_INGREDIENT_PATH)
    User_Ingredient = pd.read_csv(USER_INGREDIENT_PATH)
    Recipe = pd.read_csv(Recipe_PATH)
    User_Cuisine = pd.read_csv(User_Cuisine_PATH)
    User_FoodType = pd.read_csv(User_FoodType_PATH)
    User_CookingStyle = pd.read_csv(User_CookingStyle_PATH)
    User_Scrap = pd.read_csv(User_Scrap_PATH)
    
    return Ingredient, Recipe_Ingredient, User_Ingredient, Recipe, User_Cuisine, User_FoodType, User_CookingStyle, User_Scrap

'''