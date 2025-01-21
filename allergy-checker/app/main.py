from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.data_loader import load_ingredient, load_user_ingredient, load_recipe_ingredient
from app.ingredient_classifier import IngredientClassifier
from app.allergy_checker import AllergyChecker
from app.config import SessionLocal

# FastAPI 앱 초기화
app = FastAPI(title="Allergy Ingredient Checker API")

# DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 요청 데이터 모델 정의
class AllergyRequest(BaseModel):
    user_id: int
    recipe_id: int

# 헬스 체크 API
@app.get("/")
def health_check():
    return {"status": "API is running smoothly!"}

# 알레르기 유발 가능성 체크 API
@app.post("/check_allergy")
def check_allergy(request: AllergyRequest):
    # 데이터 로드
    user_ingredient = load_user_ingredient()
    recipe_ingredient = load_recipe_ingredient()
    ingredient = load_ingredient()

    # 데이터 가공 및 분류
    classifier = IngredientClassifier('app/rules.pkl', ingredient)
    updated_ingredient = classifier.add_classification_to_ingredients(ingredient)

    # AllergyChecker 초기화 및 결과 생성
    checker = AllergyChecker(
        Recipe_Ingredient=recipe_ingredient,
        Updated_Ingredient=updated_ingredient
    )
    result = checker.get_allergic_ingredients(request.user_id, request.recipe_id, user_ingredient)

    return {"ingredients": result}
