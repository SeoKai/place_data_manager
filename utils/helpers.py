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

# 추출하는 함수
def parse_basic_info(place, api_key):
    return {
        "place_id": place.get("place_id"),  # Google Place ID
        "location_name": place.get("name", "정보 없음"),  # 장소 이름
        "description": "",  # 설명은 초기엔 비워둠 (나중에 Selenium 등으로 채움)
        "latitude": place["geometry"]["location"]["lat"],  # 위도
        "longitude": place["geometry"]["location"]["lng"],  # 경도
        "google_rating": place.get("rating", 0.0),  # 평점 (없으면 0.0)
        "user_ratings_total": place.get("user_ratings_total", 0),  # 리뷰 수 (없으면 0)
        "place_img_url": extract_photo_url(place.get("photos", []), api_key),  # 첫 번째 사진 URL 생성
        "translated_types": [
            TYPE_TRANSLATIONS.get(tag, tag)  # 영어 태그를 한글로 변환
            for tag in place.get("types", [])
            if TYPE_TRANSLATIONS.get(tag) is not None
        ]
    }

# 상세 정보를 가져오는 함수
def parse_details(place_id, api_key):
    details = fetch_place_details(place_id, api_key)

    # 영업시간이 리스트로 들어올 경우 문자열로 합침
    opening_hours = details.get("opening_hours", "영업시간 정보 없음")
    if isinstance(opening_hours, list):
        opening_hours = ", ".join(opening_hours)

    return {
        "formatted_address": details.get("formatted_address", "정보 없음"),  # 주소
        "opening_hours": opening_hours,  # 영업시간
        "website": details.get("website", "웹사이트 없음"),  # 웹사이트 URL
        "phone_number": details.get("phone_number", "전화번호 없음")  # 전화번호
    }

# 장소 데이터를 구성하는 메인 함수
def process_place(place, api_key, region_id):
    basic = parse_basic_info(place, api_key)  # 기본 정보 추출
    details = parse_details(basic["place_id"], api_key)  # 상세 정보 조회

    # 튜플로 반환 (DB 저장용 데이터 포맷)
    return (
        basic["place_id"],
        basic["location_name"],
        basic["description"],
        basic["latitude"],
        basic["longitude"],
        basic["google_rating"],
        basic["user_ratings_total"],
        basic["place_img_url"],
        details["formatted_address"],
        details["opening_hours"],
        details["website"],
        details["phone_number"],
        region_id,  # 전달받은 지역 ID
        basic["translated_types"]
    )
