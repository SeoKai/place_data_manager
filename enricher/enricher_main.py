from enricher.db_operations import get_places_without_description, update_place_description
from enricher.selenium_scraper import fetch_description_from_google_maps

def main():
    """DB에 저장된 데이터를 활용하여 상세 설명 추가"""
    # 1. DB에서 좌표와 장소 이름 가져오기
    places = get_places_without_description()

    for place in places:
        place_id = place["place_id"]
        place_name = place["location_name"]

        # 2. Selenium으로 상세 설명 스크래핑
        description = fetch_description_from_google_maps(place_name)

        # 3. DB에 설명 업데이트
        update_place_description(place_id, description)
        print(f"장소 ID: {place_id}, 이름: {place_name} - 설명 업데이트 완료")

if __name__ == "__main__":
    main()

