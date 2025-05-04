from database.enricher_db import get_places_without_description, update_place_description
from enricher.selenium_scraper import scrape_place_description

def main(region_id=None, dry_run=False):
    """
    DB에 저장된 장소 중 설명이 없는 항목에 대해 설명 수집
    dry_run=True인 경우 DB에 저장하지 않고 결과만 출력
    """
    places = get_places_without_description(region_id=region_id)
    total = len(places)
    print(f"[INFO] 설명이 없는 장소 수: {total}개")

    success = 0

    for place in places:
        place_id = place["place_id"]
        place_name = place["location_name"]

        description = scrape_place_description(place_name)

        if description:
            if dry_run:
                print(f"[DRY-RUN] 장소 ID: {place_id}")
                print(f"  이름: {place_name}")
                print(f"  설명 미리보기: {description[:100]}...")
            else:
                update_place_description(place_id, description)
                print(f"[SUCCESS] 장소 ID: {place_id}, 이름: {place_name} - 설명 업데이트 완료")
            success += 1
        else:
            print(f"[FAIL] 설명 없음 → {place_name}")

    print("\n=== 설명 수집 요약 ===")
    print(f"총 대상: {total}개")
    print(f"성공: {success}개")
    print(f"성공률: {success / total * 100:.2f}%")
