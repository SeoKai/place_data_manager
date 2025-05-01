import requests
from config.api_config import PLACE_DETAILS_URL, TYPE_TRANSLATIONS


def extract_photo_url(photos, api_key):
    """사진 URL 생성"""
    if not photos:
        return None
    photo_reference = photos[0].get("photo_reference")
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"

def fetch_place_details(place_id, api_key):
    """Place Details API를 호출하여 디테일 데이터 가져오기"""
    params = {
        "place_id": place_id,
        "fields": "formatted_address,opening_hours,website,international_phone_number",
        "language": "ko",
        "key": api_key
    }
    response = requests.get(PLACE_DETAILS_URL, params=params)
    response.raise_for_status()
    details_data = response.json()

    # 디테일 정보 추출
    if "result" in details_data:
        result = details_data["result"]
        return {
            "formatted_address": result.get("formatted_address", "정보 없음"),
            "opening_hours": result.get("opening_hours", {}).get("weekday_text", "영업시간 정보 없음"),
            "website": result.get("website", "웹사이트 없음"),
            "phone_number": result.get("international_phone_number", "전화번호 없음")
        }
    return {}

def process_place(place, api_key, region_id):
    """Google Places + Place Details 데이터를 합쳐서 반환"""

    # 기본 정보
    place_id = place.get("place_id")
    location_name = place.get("name", "정보 없음")
    description = ""
    latitude = place["geometry"]["location"]["lat"]
    longitude = place["geometry"]["location"]["lng"]
    google_rating = place.get("rating", 0.0)
    user_ratings_total = place.get("user_ratings_total", 0)
    place_img_url = extract_photo_url(place.get("photos", []), api_key)

    # 태그 변환 (영어 → 한국어) 및 필터링
    place_types = place.get("types", [])
    translated_types = [
        TYPE_TRANSLATIONS.get(tag, tag) for tag in place_types if TYPE_TRANSLATIONS.get(tag) is not None
    ]

    # Place Details API 호출
    details = fetch_place_details(place_id, api_key)

    # opening_hours 리스트를 문자열로 변환
    opening_hours = details.get("opening_hours", "영업시간 정보 없음")
    if isinstance(opening_hours, list):  # 리스트인 경우 문자열로 병합
        opening_hours = ", ".join(opening_hours)


    # 반환
    return (
        place_id, location_name, description, latitude, longitude,
        google_rating, user_ratings_total, place_img_url,
        details.get("formatted_address", "정보 없음"),
        opening_hours,
        details.get("website", "웹사이트 없음"),
        details.get("phone_number", "전화번호 없음"),
        region_id,  # 하드코딩된 region_id 추가
        translated_types
    )