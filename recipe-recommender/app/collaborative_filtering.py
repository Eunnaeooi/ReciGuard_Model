import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from app.config import TIME_WEIGHT, DECAY_RATE, SIMILARITY_THRESHOLD

class UserBasedCollaborativeFiltering:
    def __init__(self, time_weight=TIME_WEIGHT, decay_rate=DECAY_RATE, similarity_threshold=SIMILARITY_THRESHOLD):
        self.time_weight = time_weight
        self.decay_rate = decay_rate
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def calculate_jaccard_similarity(user_profile, other_cuisine, other_foodtype, other_cookingstyle):
        other_profile = set(other_cuisine + other_foodtype + other_cookingstyle)
        if not user_profile or not other_profile:
            return 0  # 빈 집합이면 유사도 0 반환
        return len(user_profile & other_profile) / len(user_profile | other_profile)

    def create_user_profile(self, user_id, User_Cuisine, User_FoodType, User_CookingStyle):
        user_cuisine = User_Cuisine[User_Cuisine['user_id'] == user_id]['cuisine'].tolist()
        user_foodtype = User_FoodType[User_FoodType['user_id'] == user_id]['food_type'].tolist()
        user_cookingstyle = User_CookingStyle[User_CookingStyle['user_id'] == user_id]['cooking_style'].tolist()
        return set(user_cuisine + user_foodtype + user_cookingstyle)

    def recommend(self, user_id, User_Cuisine, User_FoodType, User_CookingStyle, User_Scrap, Recipe):
        user_profile = self.create_user_profile(user_id, User_Cuisine, User_FoodType, User_CookingStyle)
        other_users = User_Cuisine[User_Cuisine['user_id'] != user_id]['user_id'].unique()

        user_similarities = {
            other_user: self.calculate_jaccard_similarity(
                user_profile,
                User_Cuisine[User_Cuisine['user_id'] == other_user]['cuisine'].tolist(),
                User_FoodType[User_FoodType['user_id'] == other_user]['food_type'].tolist(),
                User_CookingStyle[User_CookingStyle['user_id'] == other_user]['cooking_style'].tolist()
            ) for other_user in other_users
        }

        similar_users = sorted(user_similarities.items(), key=lambda x: x[1], reverse=True)
        similar_user_ids = [user for user, sim in similar_users if sim >= self.similarity_threshold]

        # 비슷한 유저가 없는 경우 처리
        if not similar_user_ids:
            return pd.DataFrame(columns=['recipe_id', 'collab_score'])

        similar_scraps = User_Scrap[User_Scrap['user_id'].isin(similar_user_ids)].copy()

        similarity_scores = dict(similar_users)
        similar_scraps['similarity_score'] = similar_scraps['user_id'].map(similarity_scores)

        user_scrap_recipes = User_Scrap[User_Scrap['user_id'] == user_id]['recipe_id'].tolist()

        # 유저가 스크랩한 레시피가 없는 경우 처리
        if not user_scrap_recipes:
            return pd.DataFrame(columns=['recipe_id', 'collab_score'])

        recommended_recipes = similar_scraps[~similar_scraps['recipe_id'].isin(user_scrap_recipes)].copy()
        recommended_recipes = recommended_recipes.merge(Recipe, on='recipe_id')

        # 추천할 레시피가 없는 경우 처리
        if recommended_recipes.empty:
            return pd.DataFrame(columns=['recipe_id', 'collab_score'])

        current_date = datetime.now()
        recommended_recipes['created_at'] = pd.to_datetime(recommended_recipes['created_at'])
        recommended_recipes['days_since_created'] = (current_date - recommended_recipes['created_at']).dt.days
        recommended_recipes['time_score'] = np.exp(-recommended_recipes['days_since_created'] / self.decay_rate)

        recommended_recipes['collab_score'] = ((1 - self.time_weight) * recommended_recipes['similarity_score'] +
                                               self.time_weight * recommended_recipes['time_score'])

        scaler = MinMaxScaler()
        recommended_recipes['collab_score'] = scaler.fit_transform(recommended_recipes[['collab_score']])

        return recommended_recipes[['recipe_id', 'collab_score']].drop_duplicates().sort_values(by='collab_score', ascending=False).reset_index(drop=True)