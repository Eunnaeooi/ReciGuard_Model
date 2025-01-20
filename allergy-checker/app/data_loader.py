import pandas as pd
from sqlalchemy import create_engine
import cryptography
from app.config import host, port, user, password, database, charset

# SQLAlchemy 엔진 생성
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
)

# 데이터 로드 함수 
def load_data():

    Ingredient = pd.read_sql("SELECT * FROM ingredient", engine)
    Recipe_Ingredient = pd.read_sql("SELECT * FROM recipe_ingredient", engine)
    User_Ingredient = pd.read_sql("SELECT * FROM user_ingredient", engine)
    
    return Ingredient, Recipe_Ingredient, User_Ingredient


'''
import pandas as pd
import os

def load_data():
    DATA_PATH = "data/"
    INGREDIENT_PATH = os.path.join(DATA_PATH, "Ingredient.csv")
    RECIPE_INGREDIENT_PATH = os.path.join(DATA_PATH, "Recipe_Ingredient.csv")
    USER_INGREDIENT_PATH = os.path.join(DATA_PATH, "User_Ingredient.csv")

    Ingredient = pd.read_csv(INGREDIENT_PATH)
    Recipe_Ingredient = pd.read_csv(RECIPE_INGREDIENT_PATH)
    User_Ingredient = pd.read_csv(USER_INGREDIENT_PATH)

    return Ingredient, Recipe_Ingredient, User_Ingredient
'''