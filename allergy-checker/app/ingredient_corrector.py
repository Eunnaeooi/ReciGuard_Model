'''
import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer

# 모델과 토크나이저 로드
model = T5ForConditionalGeneration.from_pretrained("j5ng/et5-typos-corrector")
tokenizer = T5Tokenizer.from_pretrained("j5ng/et5-typos-corrector")

class IngredientCorrector:
    def __init__(self, model_name: str):
        # 모델과 토크나이저 로드
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
    
    def correct_ingredients(self, Ingredient: pd.DataFrame) -> pd.DataFrame:
        for index, row in Ingredient.iterrows():
            # 입력 텍스트
            input_text = row['ingredient']
            
            # 입력 텍스트를 토큰화
            input_encoding = self.tokenizer("오타를 수정해 주세요: " + input_text, return_tensors="pt")
            
            # 텍스트 생성 (교정된 텍스트)
            output_encoding = self.model.generate(**input_encoding, max_length=128, num_beams=5, early_stopping=True)
            corrected_text = self.tokenizer.decode(output_encoding[0], skip_special_tokens=True)
            
            # 마침표와 띄어쓰기 제거
            corrected_text = corrected_text.replace(".", "").replace(" ", "")
            
            # 교정된 텍스트로 'ingredient' 값을 대체
            Ingredient.at[index, 'ingredient'] = corrected_text
        
        return Ingredient
'''        