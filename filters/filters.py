import re

# 한글 포함 여부 판단
KOREAN_REGEX = re.compile(r'[\uac00-\ud7a3]')

# 음식점 유형
FOOD_TYPES = {"restaurant", "cafe", "bar", "bakery"}

# 기본 필터 기준
DEFAULT_MIN_RATING = 4.0
DEFAULT_MIN_REVIEWS = 500

def is_korean(text):
    """문자열에 한글이 포함되어 있는지 확인"""
    if not text:
        return False
    return bool(KOREAN_REGEX.search(text))

def has_min_rating(place, min_rating):
    """장소의 평점이 최소 조건을 만족하는지 확인"""
    return place.get("rating", 0.0) >= min_rating

def has_min_reviews(place, min_reviews):
    """장소의 리뷰 수가 최소 조건을 만족하는지 확인"""
    return place.get("user_ratings_total", 0) >= min_reviews

def is_type_excluded(place, excluded_types):
    """장소 유형이 제외된 목록에 포함되는지 확인"""
    place_types = {ptype.lower() for ptype in place.get("types", [])}
    return any(excluded in place_types for excluded in excluded_types)

def is_food_place(place_types):
    """해당 장소가 음식점 유형에 해당하는지 확인"""
    return bool(FOOD_TYPES & set(place_types))  # set 교집합 확인


def filter_place(
    place,
    min_rating=DEFAULT_MIN_RATING,
    min_reviews=DEFAULT_MIN_REVIEWS,
    excluded_types=None
):
    """
    장소 필터링
    - 평점, 리뷰 수가 기준 이상
    - 특정 유형은 제외
    - 음식점이면 기준 완화
    - 한글 이름 포함 여부
    """
    if excluded_types is None:
        excluded_types = {"lodging"}

    place_types = place.get("types", [])
    location_name = place.get("name", "")

    # 음식점인 경우 필터 기준 완화
    if is_food_place(place_types):
        min_rating = 3.5
        min_reviews = 200

    return (
        has_min_rating(place, min_rating) and           # 평점 기준 충족
        has_min_reviews(place, min_reviews) and         # 최소 리뷰 수 기준 충족
        not is_type_excluded(place, excluded_types) and # 제외된 유형이 아님
        is_korean(location_name)                        # 장소 이름에 한글 포함
    )
