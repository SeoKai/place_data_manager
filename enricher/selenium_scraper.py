from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 설명이 들어 있을 수 있는 div 셀렉터 목록
DESCRIPTION_SELECTORS = [
    ".PYvSYb",  # 일반 설명
    ".hfpxzc"   # 드물게 여기에 설명이 직접 포함됨
]


def get_driver():
    """Chrome WebDriver 생성 (시크릿 모드, 창 표시)"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def search_place(driver, place_name):
    """Google Maps에서 검색창에 장소 이름 입력하고 검색"""
    driver.get("https://www.google.com/maps")
    time.sleep(1.5)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()

    # 일본 지역 기반으로 검색 정확도 향상
    search_query = f"{place_name}, Japan"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # 검색 결과 또는 패널 로딩까지 약간의 시간 확보
    time.sleep(2)


def extract_description(driver):
    """설명 텍스트가 들어 있을 수 있는 여러 셀렉터를 순차적으로 검사"""
    for selector in DESCRIPTION_SELECTORS:
        try:
            print(f"[DEBUG] 설명 시도: {selector}")
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            text = element.text.strip()
            if text:
                print(f"[SUCCESS] 설명 추출 성공 ({selector})")
                return text
        except Exception:
            print(f"[INFO] {selector} 설명 없음 → 다음 시도")
            continue

    print("[WARNING] 설명 추출 실패 - 모든 시도 실패")
    return None


def scrape_place_description(place_name):
    """Google Maps에서 장소 설명을 자동으로 스크래핑"""
    driver = get_driver()
    description = None

    try:
        print(f"[INFO] 검색 시작: {place_name}")
        search_place(driver, place_name)

        print(f"[INFO] 설명 추출 시도: {place_name}")
        description = extract_description(driver)

        if description:
            print(f"[SUCCESS] 설명 수집 완료: {place_name}")
        else:
            print(f"[WARNING] 설명 없음: {place_name}")

    except Exception as e:
        print(f"[ERROR] Selenium 오류 발생: {place_name} | {e}")

    finally:
        driver.quit()

    return description
