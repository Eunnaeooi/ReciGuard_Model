import pandas as pd
from app.config import engine

# 데이터 로드 함수
def load_ingredient():
    """ingredient 테이블"""
    return pd.read_sql("SELECT * FROM ingredient", engine)

def load_user_ingredient():
    """user_ingredient 테이블"""
    return pd.read_sql("SELECT * FROM user_ingredient", engine)

def load_recipe_ingredient():
    """recipe_ingredient 테이블"""
    return pd.read_sql("SELECT * FROM recipe_ingredient", engine)
