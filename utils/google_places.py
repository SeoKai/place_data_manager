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