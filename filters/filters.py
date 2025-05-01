import re

KOREAN_REGEX = re.compile(r'[\uac00-\ud7a3]')

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
    """장소 유형이 제외된 유형에 포함되는지 확인"""
    place_types = place.get("types", [])
    place_types = [ptype.lower() for ptype in place_types]  # 소문자로 변환
    return any(excluded_type in place_types for excluded_type in excluded_types)

def filter_place(place, min_rating=4.0, min_reviews=500, excluded_types=None):
    """
    평점, 리뷰 수 및 제외할 장소 유형 기준으로 장소 필터링
    :param place: 장소 데이터
    :param min_rating: 최소 평점
    :param min_reviews: 최소 리뷰 수
    :param excluded_types: 제외할 장소 유형 리스트
    :return: 필터를 통과하면 True, 그렇지 않으면 False
    """
    if excluded_types is None:
        excluded_types = ["lodging"]
    location_name = place.get("name", "")
    place_types = place.get("types", [])

    # 음식점 관련 유형
    food_types = ["restaurant", "cafe", "bar", "bakery"]

    # 음식점 기준 완화 적용
    if any(food_type in place_types for food_type in food_types):
        min_rating = 3.5  # 음식점 최소 평점
        min_reviews = 200  # 음식점 최소 리뷰 수

    return (
        has_min_rating(place, min_rating)  # 평점 기준 충족
        and has_min_reviews(place, min_reviews)  # 최소 리뷰 수 기준 충족
        and not is_type_excluded(place, excluded_types)  # 제외된 유형이 아님
        and is_korean(location_name)  # 장소 이름에 한글 포함
    )
