from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# AWS MySQL 연결 정보
host = "reciguard-db.czouas0eqnqo.ap-northeast-2.rds.amazonaws.com"
port = 3306
user = 'reciguard'
password = 'tavereciguard'
database = 'reciguard'
charset = 'utf8mb4'

# SQLAlchemy 엔진 생성
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 하이퍼파라미터
WEIGHT_CUISINE = 0.6
WEIGHT_FOODTYPE = 0.25
WEIGHT_COOKINGSTYLE = 0.15

TIME_WEIGHT = 0.3
DECAY_RATE = 7
SIMILARITY_THRESHOLD = 0.4

CONTENT_WEIGHT = 0.9
COLLAB_WEIGHT = 0.1
