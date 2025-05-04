from config.place_regions import REGION_CONFIGS
from core.collector import collect_places
from enricher.enricher_main import enrich_descriptions


def main():
    region = REGION_CONFIGS["교토"]  # 원하는 지역으로 수정

    print("[STEP 1] 장소 수집 시작")
    collect_places(**region)

    print("[STEP 2] 설명 수집 시작")
    enrich_descriptions()

    print("[DONE] 전체 작업 완료")


if __name__ == "__main__":
    main()
