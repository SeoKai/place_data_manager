# 태그 상수
PLACE_TYPES = [
    "tourist_attraction", "park", "zoo", "aquarium", "amusement_park",  # 관광명소
    "restaurant", "cafe", "bar", "bakery",                              # 음식
    "historical_landmark", "place_of_worship",                          # 랜드마크
    "museum", "art_gallery",                                            # 문화
    "shopping_mall", "store", "market"                                  # 쇼핑
]

# 지역별 설정
REGION_CONFIGS = {
    "도쿄": {
        "region_id": 1,                     # 도시코드
        "location": "35.6842,139.7574",     # 위도, 경도
        "radius": 1000,                     # 주위 반경 1000 == 1KM
        "types": PLACE_TYPES                # 태그 타입
    },
    "후쿠오카": {
        "region_id": 2,                     # 도시코드
        "location": "33.5897, 130.4199",     # 위도, 경도
        "radius": 1000,                     # 주위 반경 1000 == 1KM
        "types": PLACE_TYPES                # 태그 타입
    },
    "오사카": {
        "region_id": 3,                     # 도시코드
        "location": "34.6707, 135.4982",     # 위도, 경도
        "radius": 1000,                     # 주위 반경 1000 == 1KM
        "types": PLACE_TYPES                # 태그 타입
    },
    "교토": {
        "region_id": 4,                     # 도시코드
        "location": "34.9854,135.7587",     # 위도, 경도
        "radius": 1000,                     # 주위 반경 1000 == 1KM
        "types": PLACE_TYPES                # 태그 타입
    }
}