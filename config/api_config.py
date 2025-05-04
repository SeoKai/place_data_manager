# config/api_config.py

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 값 가져오기
API_KEY = os.getenv("GOOGLE_API_KEY")
LANGUAGE = os.getenv("LANGUAGE", "ko")

NEARBY_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

TYPE_TRANSLATIONS = {
    "tourist_attraction": "관광지",
    "park": "공원",
    "zoo": "동물원",
    "aquarium": "아쿠아리움",
    "amusement_park": "놀이공원",
    "restaurant": "음식점",
    "cafe": "카페",
    "bar": "바",
    "bakery": "베이커리",
    "historical_landmark": "사적지",
    "place_of_worship": "종교시설",
    "museum": "박물관",
    "art_gallery": "미술관",
    "shopping_mall": "쇼핑몰",
    "store": "상점",
    "market": "시장"
}