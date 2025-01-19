from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from app.hybrid_recommender import HybridRecommender
from app.recipe_filter import RecipeFilter
from app.data_loader import load_data

app = FastAPI()

# 데이터 로드
Ingredient, Recipe_Ingredient, User_Ingredient, Recipe, User_Cuisine, User_FoodType, User_CookingStyle, User_Scrap = load_data()

'''
# csv 테스트 전처리!
from datetime import datetime
User_Scrap['created_at'] = User_Scrap['created_at'].apply(
    lambda x: datetime.now() if x == 'NOW()' else pd.to_datetime(x)
)
'''


# RecipeFilter 초기화
recipe_filter = RecipeFilter(rules_file_path="app/rules.pkl")  

# HybridRecommender 초기화
hybrid_recommender = HybridRecommender()


# 서버 상태 확인 엔드포인트
@app.get("/")
def root():
    return {"message": "Hybrid Recommendation System is running."}

# 추천 요청 모델
class RecommendationRequest(BaseModel):
    user_id: int


# 추천 요청 엔드포인트
@app.post("/recommend")
def recommend_recipe(request: RecommendationRequest):
    try:
        # 레시피 필터링
        Filtered_Recipe = recipe_filter.filter_recipes(
            user_id=request.user_id,
            User_Ingredient=User_Ingredient,
            Ingredient=Ingredient,
            Recipe_Ingredient=Recipe_Ingredient,
            Recipe=Recipe
        )
        
        # 하이브리드 추천 실행
        recommendation = hybrid_recommender.recommend(
            request.user_id,
            User_Cuisine,
            User_FoodType,
            User_CookingStyle,
            User_Scrap,
            Filtered_Recipe
        )
        return {"recipe_id": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    