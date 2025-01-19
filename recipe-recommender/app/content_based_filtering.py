from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from app.config import WEIGHT_CUISINE, WEIGHT_FOODTYPE, WEIGHT_COOKINGSTYLE

class ContentBasedRecommenderEmbedding:
    def __init__(self, weight_cuisine=WEIGHT_CUISINE, weight_foodtype=WEIGHT_FOODTYPE, weight_cookingstyle=WEIGHT_COOKINGSTYLE, embedding_dim=8):
        self.weight_cuisine = weight_cuisine
        self.weight_foodtype = weight_foodtype
        self.weight_cookingstyle = weight_cookingstyle
        self.embedding_dim = embedding_dim
        self.word2vec_model = None

    def embed_recipe(self, features):
        feature_list = str(features).split()
        embeddings = [self.word2vec_model.wv[feature] for feature in feature_list if feature in self.word2vec_model.wv]
        return np.mean(embeddings, axis=0) if embeddings else np.zeros(self.embedding_dim)

    def fit_word2vec(self, Recipe):
        Recipe['combined_features'] = Recipe['cuisine'].fillna('') + ' ' + Recipe['food_type'].fillna('') + ' ' + Recipe['cooking_style'].fillna('')
        all_features = Recipe['combined_features'].apply(lambda x: x.split()).tolist()
        self.word2vec_model = Word2Vec(sentences=all_features, vector_size=self.embedding_dim, window=5, min_count=1, workers=4)

    def create_user_profile_embedding(self, user_id, User_Cuisine, User_FoodType, User_CookingStyle):
        # 유저별 선호 데이터를 리스트로 변환
        user_cuisine = User_Cuisine[User_Cuisine['user_id'] == user_id]['cuisine'].tolist()
        user_foodtype = User_FoodType[User_FoodType['user_id'] == user_id]['food_type'].tolist()
        user_cookingstyle = User_CookingStyle[User_CookingStyle['user_id'] == user_id]['cooking_style'].tolist()

        # Word2Vec 임베딩 벡터 추출
        cuisine_embeddings = [self.word2vec_model.wv[feature] for feature in user_cuisine if feature in self.word2vec_model.wv]
        foodtype_embeddings = [self.word2vec_model.wv[feature] for feature in user_foodtype if feature in self.word2vec_model.wv]
        cookingstyle_embeddings = [self.word2vec_model.wv[feature] for feature in user_cookingstyle if feature in self.word2vec_model.wv]

        # 항목별 평균 벡터 계산
        cuisine_vector = np.mean(cuisine_embeddings, axis=0) if cuisine_embeddings else np.zeros(self.embedding_dim)
        foodtype_vector = np.mean(foodtype_embeddings, axis=0) if foodtype_embeddings else np.zeros(self.embedding_dim)
        cookingstyle_vector = np.mean(cookingstyle_embeddings, axis=0) if cookingstyle_embeddings else np.zeros(self.embedding_dim)

        # 가중치 적용 및 최종 유저 임베딩 생성
        user_profile_embedding = (self.weight_cuisine * cuisine_vector +
                                self.weight_foodtype * foodtype_vector +
                                self.weight_cookingstyle * cookingstyle_vector)

        return user_profile_embedding

    def recommend(self, user_id, User_Cuisine, User_FoodType, User_CookingStyle, Recipe):
        self.fit_word2vec(Recipe)
        user_profile_embedding = self.create_user_profile_embedding(user_id, User_Cuisine, User_FoodType, User_CookingStyle)

        recipe_embeddings = Recipe['combined_features'].apply(lambda x: self.embed_recipe(x))
        recipe_embeddings_matrix = np.vstack(recipe_embeddings.values)
        similarities = cosine_similarity([user_profile_embedding], recipe_embeddings_matrix)[0]
        Recipe['content_score'] = similarities

        scaler = MinMaxScaler()
        Recipe['content_score'] = scaler.fit_transform(Recipe[['content_score']])

        return Recipe[['recipe_id', 'content_score']].sort_values(by='content_score', ascending=False)
