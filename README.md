# `Place Data Manager`

> 지역 기반의 장소 데이터를 Google Places API로 수집하고,
> 부족한 설명 정보를 Selenium을 통해 Google Maps에서 자동으로 보완하여
> **MySQL 데이터베이스에 저장하는 자동화 시스템 입니다.**

![장소수집](https://github.com/user-attachments/assets/729b968f-4537-432c-965e-d07430f516dd)

## 구동화면

> **추가예정**

---
### CLI 기반 실행

> 본 프로젝트는 단순 실행이 아닌, 지역 설정, 옵션 조절 등이 가능한
> **CLI(Command Line Interface) 프로그램**입니다.

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

## E-R 다이어그램
![ERD.PNG](..%2F..%2F..%2F..%2FERD.PNG)
> 본장소와 태그 간의 N:M 관계를 지원하기 위해 다음과 같은 테이블 구조로 구성되어 있습니다
> - **tbl_location**: Google Places API를 통해 수집된 장소의 상세 정보를 저장합니다.
> - **tbl_tag**: 장소에 부여할 수 있는 태그 목록을 관리합니다.
> - **tbl_location_tag**: 장소와 태그 간의 다대다(N:M) 관계를 연결하는 매핑 테이블입니다.

---
