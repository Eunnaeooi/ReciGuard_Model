import pickle
from fuzzywuzzy import fuzz
import pandas as pd
from app.config import SIMILARITY_THRESHOLD

class IngredientClassifier:
    def __init__(self, rules_path, Ingredient, similarity_threshold=SIMILARITY_THRESHOLD):
        """초기화 메서드"""
        with open(rules_path, "rb") as file:
            self.rules = pickle.load(file)
        self.ingredient_data = Ingredient
        self.similarity_threshold = similarity_threshold

    def classify_and_map_ingredient(self, ingredient):
        """알레르기 분류 및 유사도 계산"""
        allergens_to_avoid = []
        for allergen_group, ingredients in self.rules.items():
            for known_ingredient in ingredients:
                score = fuzz.ratio(ingredient, known_ingredient)
                if score > self.similarity_threshold:
                    allergens_to_avoid.append((allergen_group, score))

        allergens_to_avoid = sorted(allergens_to_avoid, key=lambda x: x[1], reverse=True)
        if allergens_to_avoid:
            classification, score = allergens_to_avoid[0]
        else:
            classification, score = None, 0

        if classification:
            match = self.ingredient_data[self.ingredient_data["ingredient"] == classification]
            ingredient_id_from_name = int(match["ingredient_id"].values[0]) if not match.empty else None
        else:
            ingredient_id_from_name = None

        return pd.Series([classification, score, ingredient_id_from_name])

    def add_classification_to_ingredients(self, Ingredient):
        """Ingredient에 분류 결과 추가"""
        Ingredient[['ingredient_classification', 'score', 'ingredient_id_from_name']] = Ingredient['ingredient'].apply(
            self.classify_and_map_ingredient
        )
        Ingredient['ingredient_id_from_name'] = Ingredient['ingredient_id_from_name'].astype('Int64')
        Updated_Ingredient = Ingredient
        return Updated_Ingredient
