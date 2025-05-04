# `Place Data Manager`

> 지역 기반의 장소 데이터를 Google Places API로 수집하고,
> 부족한 설명 정보를 Selenium을 통해 Google Maps에서 자동으로 보완하여
> **MySQL 데이터베이스에 저장하는 자동화 시스템**

---

## 폴더 구조

```
place_data_manager/
├── config/
│   ├── api_config.py         # API 키 관리
│   ├── db_config.py          # DB 키 관리
│   └── place_regions.py      # 지역 좌표 및 설정
├── core/
│   └── collector.py          # 장소 수집 로직
├── enricher/
│   ├── enricher_main.py      # 설명 수집 메인
│   └── selenium_scraper.py   # 셀레니움 크롤링 모듈
├── database/
│   ├── db_connection.py      # MySQL 연결 함수
│   ├── cursor_manager.py     # DB 커서 컨텍스트 매니저
│   ├── location_db.py        # 장소 및 태그 저장 관련 DB 함수
│   └── enricher_db.py        # 설명이 없는 장소 조회 및 업데이트
├── filters/
│   └── filters.py            # 장소 필터링 조건
├── utils/
│   ├── google_places.py      # Google API 통신
│   └── helpers.py            # 장소 파싱 유틸
├── main.py                   # 전체 실행 CLI 진입점
├── run_collector.bat         # Windows CLI 실행 스크립트
└── .env                      # API 키 등 환경 변수
```
