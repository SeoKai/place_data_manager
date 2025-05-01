# core/collector.py

from config.api_config import API_KEY
from database.db_operations import save_to_database, save_tags, save_location_tags
from utils.google_places import fetch_all_places
from utils.helpers import process_place
from filters.filters import filter_place


def collect_places(region_id, location, radius, types):
    """
    Google Places API로 장소 데이터를 수집 → 필터링 → DB 저장
    """
    all_places = []
    for place_type in types:
        places = fetch_all_places(location, radius, place_type)
        all_places.extend(places)

    # 중복 제거
    unique_places = {place["place_id"]: place for place in all_places}.values()

    # 필터링
    filtered_places = [place for place in unique_places if filter_place(place)]

    # DB 저장
    for place in filtered_places:
        try:
            data = process_place(place, API_KEY, region_id)
            location_id = save_to_database(data)
            tags = data[-1]
            tag_ids = save_tags(tags)
            save_location_tags(location_id, tag_ids)
        except Exception as e:
            print(f"[ERROR] {place.get('name', 'Unknown')} 저장 실패: {e}")
