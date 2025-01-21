from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.data_loader import load_data
from app.hybrid_recommender import HybridRecommender
from app.recipe_filter import RecipeFilter
from app.config import SessionLocal

app = FastAPI()

# DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def recommend_recipe(request: RecommendationRequest, db: Session = Depends(get_db)):
    try:
        # 데이터 로드
        Ingredient, Recipe_Ingredient, User_Ingredient, Recipe, User_Cuisine, User_FoodType, User_CookingStyle, User_Scrap = load_data(db)

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
