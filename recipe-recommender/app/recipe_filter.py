import pandas as pd
import pickle

class RecipeFilter:
    def __init__(self, rules_file_path):
        self.rules_file_path = rules_file_path
        self.recipe_ingredients_cache = None  # 병합된 데이터 캐싱

    def load_rules(self):
        # rules 파일 로드
        with open(self.rules_file_path, "rb") as file:
            return pickle.load(file)

    def get_user_ingredients(self, user_id, User_Ingredient, Ingredient):
        # 사용자 재료 가져오기
        user_ingredients_with_names = User_Ingredient[User_Ingredient['user_id'] == user_id].merge(
            Ingredient,
            how='left',
            left_on='ingredient_id',
            right_on='ingredient_id'
        )
        return [ingredient.strip().lower() for ingredient in user_ingredients_with_names['ingredient'].tolist()]

    def match_and_map_categories(self, user_ingredient_names, rules, Ingredient):
        # 사용자 재료와 rules 매칭 및 ID 매핑
        matching_categories = {}
        ingredient_to_id = dict(zip(Ingredient['ingredient'], Ingredient['ingredient_id']))
        matching_categories_with_ids = {}

        for category, ingredients in rules.items():
            normalized_ingredients = [ingredient.strip().lower() for ingredient in ingredients]
            matching_ingredients = [ingredient for ingredient in user_ingredient_names if ingredient in normalized_ingredients]
            if matching_ingredients:
                matching_categories[category] = ingredients
                matching_categories_with_ids[category] = {
                    'ingredients': ingredients,
                    'ingredient_ids': [ingredient_to_id.get(ingredient, None) for ingredient in ingredients]
                }
        return matching_categories_with_ids

    def prepare_recipe_ingredients(self, Recipe_Ingredient, Ingredient):
        # Recipe_Ingredient와 Ingredient 병합 (캐싱)
        if self.recipe_ingredients_cache is None:
            self.recipe_ingredients_cache = Recipe_Ingredient.merge(
                Ingredient,
                how='left',
                left_on='ingredient_id',
                right_on='ingredient_id'
            )
        return self.recipe_ingredients_cache

    def filter_excluded_recipes(self, matching_categories_with_ids, Recipe_Ingredient):
        # 제외할 recipe_id 추출
        excluded_ingredient_ids = set(
            ingredient_id
            for data in matching_categories_with_ids.values()
            for ingredient_id in data['ingredient_ids']
        )
        excluded_recipe_ids = Recipe_Ingredient[
            Recipe_Ingredient['ingredient_id'].isin(excluded_ingredient_ids)
        ]['recipe_id'].unique()
        return excluded_recipe_ids

    def add_ingredients_to_recipes(self, Recipe, excluded_recipe_ids):
        # 필터링된 레시피에 재료 추가
        remaining_recipes = Recipe[~Recipe['recipe_id'].isin(excluded_recipe_ids)]
        remaining_recipes = remaining_recipes[remaining_recipes['recipe_id'] != 982]

        # 재료 추가
        remaining_recipes['ingredients'] = remaining_recipes['recipe_id'].apply(
            lambda recipe_id: self.recipe_ingredients_cache[
                self.recipe_ingredients_cache['recipe_id'] == recipe_id
            ]['ingredient'].tolist()
        )
        return remaining_recipes

    def filter_recipes(self, user_id, User_Ingredient, Ingredient, Recipe_Ingredient, Recipe):
        # rules 로드
        rules = self.load_rules()

        # 사용자 재료 가져오기
        user_ingredient_names = self.get_user_ingredients(user_id, User_Ingredient, Ingredient)

        # 사용자 재료 매칭 및 ID 매핑
        matching_categories_with_ids = self.match_and_map_categories(user_ingredient_names, rules, Ingredient)

        # Recipe_Ingredient 준비 (병합된 데이터 캐싱)
        self.prepare_recipe_ingredients(Recipe_Ingredient, Ingredient)

        # 제외할 recipe_id 식별
        excluded_recipe_ids = self.filter_excluded_recipes(matching_categories_with_ids, self.recipe_ingredients_cache)

        # 필터링된 레시피 반환
        return self.add_ingredients_to_recipes(Recipe, excluded_recipe_ids)