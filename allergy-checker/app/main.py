from fastapi import FastAPI
from pydantic import BaseModel
from app.data_loader import load_data
# from app.ingredient_corrector import IngredientCorrector
from app.ingredient_classifier import IngredientClassifier
from app.allergy_checker import AllergyChecker


app = FastAPI(title="Allergy Ingredient Checker API")


# 데이터 로드 및 모델 초기화
Ingredient, Recipe_Ingredient, User_Ingredient = load_data()

classifier = IngredientClassifier('app/rules.pkl', Ingredient)
Updated_Ingredient = classifier.add_classification_to_ingredients(Ingredient)

checker = AllergyChecker(
    Recipe_Ingredient=Recipe_Ingredient,
    Updated_Ingredient=Updated_Ingredient
)


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
    result = checker.get_allergic_ingredients(request.user_id, request.recipe_id, User_Ingredient)
    return {"ingredients": result}
