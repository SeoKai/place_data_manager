# core/collector.py

from config.api_config import API_KEY
from database.location_db import save_to_database, save_tags, save_location_tags
from utils.google_places import fetch_all_places
from utils.helpers import process_place
from filters.filters import filter_place

def collect_places(region_id, location, radius, types, dry_run=False):
    """
    Google Places API로 장소 데이터를 수집 → 필터링 → DB 저장 또는 콘솔 출력
    """
    all_places = []
    for place_type in types:
        places = fetch_all_places(location, radius, place_type)
        all_places.extend(places)

    # 중복 제거
    unique_places = {place["place_id"]: place for place in all_places}.values()

    # 필터링
    filtered_places = [place for place in unique_places if filter_place(place)]

    # 결과 처리
    for place in filtered_places:
        try:
            data = process_place(place, API_KEY, region_id)
            tags = data[-1]

            if dry_run:
                print("[DRY-RUN] 수집된 장소 정보:")
                print(f"  이름: {data[1]}")
                print(f"  위도/경도: {data[3]}, {data[4]}")
                print(f"  태그: {tags}")
                print(f"  주소: {data[8]}")
                print("-" * 40)
                continue

            # 실제 DB 저장
            location_id = save_to_database(data)
            tag_ids = save_tags(tags)
            save_location_tags(location_id, tag_ids)

        except Exception as e:
            print(f"[ERROR] {place.get('name', 'Unknown')} 저장 실패: {e}")
