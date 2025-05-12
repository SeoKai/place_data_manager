# `Place Data Manager`

> 지역 기반의 장소 데이터를 Google Places API로 수집하고,
> 부족한 설명 정보를 Selenium을 통해 Google Maps에서 자동으로 보완하여
> **MySQL 데이터베이스에 저장하는 자동화 시스템 입니다.**

---

## ScreenShot

![장소수집](https://github.com/user-attachments/assets/729b968f-4537-432c-965e-d07430f516dd)

---

## 구동 화면 예시

### 수집 시작 단계

> **지역 설정 후 수집 실행**

![1-2239-60-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/9499b37f-7d58-4fab-a071-96da9c3cca20)

- 사용자 입력을 통해 지역을 설정하고 실행  
- `--dry-run`, `--skip-description` 등의 옵션도 사용 가능

---

### 설명 추출 성공

![1-2239-60-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/6275e300-b008-4c87-9fd2-b5fbad84a96c)

- Google Maps에서 설명 텍스트 추출 성공 시, DB에 업데이트  
- 콘솔에 장소 ID, 이름, 설명 미리보기가 표시됨

---

### 설명 추출 실패

> **구글맵에 상세 설명이 없는 경우 추출되지 않습니다**

![1-2239-60-ezgif com-video-to-gif-converter (2)](https://github.com/user-attachments/assets/88a2aef3-706b-42e1-9077-328d88fcc1b2)

- 설명이 존재하지 않으면 실패 메시지를 출력하고 넘어감

---

### 수집 결과 요약

> **모든 설명 추출이 완료된 후 결과를 요약하여 출력합니다**

![결과 요약](https://github.com/user-attachments/assets/943fbe6f-ffb4-48de-9983-54297171a219)

- 전체 대상 수
- 성공/실패 건수
- 성공률 등 요약 통계 출력



## 실행 방법

### 1. 환경 변수 설정 (`.env`)

```env
GOOGLE_API_KEY=당신의_구글_API_키
LANGUAGE=ko

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=placedata
```

`.env` 파일을 루트 디렉토리에 생성하고 위와 같이 설정합니다.

---

### 2. 라이브러리 설치

```bash
pip install -r requirements.txt
```

---

### 3. CLI 실행 예시

```bash
# 도쿄 지역 수집 (DB 저장 포함)
python main.py --region 도쿄

# dry-run 실행 (DB 저장 없이 출력만)
python main.py --region 오사카 --dry-run

# 설명 수집 생략
python main.py --region 후쿠오카 --skip-description
```

---

### 4. `.bat` 파일을 통한 실행 (Windows 전용)

`run_collector.bat` 파일을 더블클릭하면 자동으로 CLI 실행됩니다.

```bat
@echo off
set /p REGION="수집할 지역명을 입력하세요: "
set /p DRY="dry-run 모드로 실행할까요? (y/n): "
set /p SKIP_DESC="설명 수집을 건너뛸까요? (y/n): "

set DRY_FLAG=
if /I "%DRY%"=="y" set DRY_FLAG=--dry-run

set SKIP_FLAG=
if /I "%SKIP_DESC%"=="y" set SKIP_FLAG=--skip-description

python main.py --region %REGION% %DRY_FLAG% %SKIP_FLAG%
pause
```

---

### 위치나 반경, 태그를 커스터마이징하고 싶다면?

`config/place_regions.py` 파일을 수정하면 수집 위치(위도/경도), 반경, 장소 유형을 자유롭게 설정할 수 있습니다.

**EX)**

```python
REGION_CONFIGS = {
    "삿포로": {
        "region_id": 5,
        "location": "43.0618,141.3545",
        "radius": 2000,
        "types": ["tourist_attraction", "cafe", "museum"]
    }
}
```

```bash
python main.py --region 삿포로
```

기존 지역 외에 **새로운 지역명으로 바로 실행 가능**하며, radius는 최대 50000m까지 가능합니다.


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

![ERD](https://github.com/user-attachments/assets/b823e6fb-8473-44de-b340-d328380f32d0)

> 본장소와 태그 간의 N:M 관계를 지원하기 위해 다음과 같은 테이블 구조로 구성되어 있습니다
- **tbl_location**: Google Places API를 통해 수집된 장소의 상세 정보를 저장합니다.
- **tbl_tag**: 장소에 부여할 수 있는 태그 목록을 관리합니다.
- **tbl_location_tag**: 장소와 태그 간의 다대다(N:M) 관계를 연결하는 매핑 테이블입니다.

---
