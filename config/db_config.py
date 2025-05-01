import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 값 가져오기
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": DB_PASSWORD,  # MySQL 비밀번호
    "database": "placedata"  # 데이터베이스 이름
}
