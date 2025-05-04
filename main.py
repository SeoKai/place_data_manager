# main.py

import argparse
from config.place_regions import REGION_CONFIGS
from core.collector import collect_places
from enricher.enricher_main import main as enrich_descriptions

def main():
    parser = argparse.ArgumentParser(description="장소 수집 및 설명 enrichment 실행")
    parser.add_argument("--region", required=True, help="수집할 지역명 (예: 도쿄, 교토, 오사카, 후쿠오카)")
    parser.add_argument("--dry-run", action="store_true", help="DB에 저장하지 않고 출력만 합니다")
    parser.add_argument("--skip-description", action="store_true", help="장소만 수집하고 설명은 건너뜁니다")
    args = parser.parse_args()

    region_name = args.region
    if region_name not in REGION_CONFIGS:
        print(f"[ERROR] '{region_name}' 지역은 존재하지 않습니다.")
        print(f"[INFO] 사용 가능한 지역: {', '.join(REGION_CONFIGS.keys())}")
        return

    region = REGION_CONFIGS[region_name]

    print(f"[STEP 1] 장소 수집 시작: {region_name}")
    collect_places(**region, dry_run=args.dry_run)

    if not args.skip_description:
        print(f"[STEP 2] 설명 수집 시작: {region_name}")
        enrich_descriptions(region_id=region["region_id"], dry_run=args.dry_run)

    print("[DONE] 전체 작업 완료")

if __name__ == "__main__":
    main()
