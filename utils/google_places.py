import time
import requests
from config.api_config import API_KEY, LANGUAGE, NEARBY_SEARCH_URL, PLACE_DETAILS_URL

def fetch_all_places(location, radius=10000, place_type="tourist_attraction"):
    """Google Places API를 사용하여 모든 페이지의 장소 데이터를 가져오기"""
    all_results = []
    params = {
        "location": location,
        "radius": radius,
        "type": place_type,
        "language": LANGUAGE,  # 한국어 설정
        "key": API_KEY
    }

    while True:
        response = requests.get(NEARBY_SEARCH_URL, params=params)
        response.raise_for_status()  # 요청 실패 시 예외 발생
        data = response.json()

        # 현재 페이지의 결과를 추가
        all_results.extend(data.get("results", []))

        # 다음 페이지 토큰 확인
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break  # 다음 페이지가 없으면 종료

        # 토큰 활성화를 위해 대기 후 다음 요청
        params["pagetoken"] = next_page_token
        time.sleep(2)  # 최소 2초 대기 필요

    return all_results

def fetch_place_details(place_id):
    """Place Details API를 호출하여 장소 세부 정보를 가져오기"""
    params = {
        "place_id": place_id,
        "fields": "formatted_address,opening_hours,website,international_phone_number",
        "language": LANGUAGE,
        "key": API_KEY
    }
    try:
        response = requests.get(PLACE_DETAILS_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "result" in data:
            result = data["result"]
            return {
                "formatted_address": result.get("formatted_address", "정보 없음"),
                "opening_hours": result.get("opening_hours", {}).get("weekday_text", "영업시간 정보 없음"),
                "website": result.get("website", "웹사이트 없음"),
                "phone_number": result.get("international_phone_number", "전화번호 없음")
            }
    except Exception as e:
        print(f"[ERROR] Details API 호출 실패 (place_id: {place_id}): {e}")
    return None
