from core.collector import collect_places
from config.place_regions import REGION_CONFIGS

def main():
    # 수집할 도시 이름
    config = REGION_CONFIGS["도쿄"]
    collect_places(**config)

if __name__ == "__main__":
    main()
