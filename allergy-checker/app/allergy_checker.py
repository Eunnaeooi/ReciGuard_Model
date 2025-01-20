import pandas as pd

class AllergyChecker:
    def __init__(self, Recipe_Ingredient, Updated_Ingredient):
        """Recipe_Ingredient와 Updated_Ingredient 병합"""
        self.new_Recipe_Ingredient = Recipe_Ingredient.merge(
            Updated_Ingredient,
            how='left',
            left_on='ingredient_id',
            right_on='ingredient_id'
        )

    def get_allergic_ingredients(self, user_id, recipe_id, User_Ingredient):
        """사용자와 레시피의 알레르기 성분 반환"""
        # User_Ingredient에서 특정 user_id의 알레르기 재료 필터링
        user_allergens = User_Ingredient[User_Ingredient['user_id'] == user_id]

        # 결측치 제거
        user_allergens = user_allergens.dropna(subset=['ingredient_id'])
        self.new_Recipe_Ingredient = self.new_Recipe_Ingredient.dropna(subset=['ingredient_id', 'ingredient_id_from_name'])

        # recipe_id로 필터링
        recipe_components = self.new_Recipe_Ingredient[self.new_Recipe_Ingredient['recipe_id'] == recipe_id]

        # 병합
        matched_allergens = pd.merge(
            user_allergens,
            recipe_components,
            how='inner',
            left_on='ingredient_id',
            right_on='ingredient_id_from_name'
        )

        # 결과 반환
        result = matched_allergens[['ingredient']].drop_duplicates()

        return result['ingredient'].tolist()

