from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def setup_driver():
    """webdriver-manager를 사용하여 ChromeDriver 자동 설정"""
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


def fetch_description_from_google_maps(place_name):
    """Selenium을 사용하여 Google Maps에서 장소 설명 스크래핑"""
    driver = setup_driver()
    driver.get("https://www.google.com/maps")

    try:
        # 검색창 초기화 및 검색
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_query = f"{place_name}, Japan"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        # 검색 결과 로드 및 클릭
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
        )

        if len(results) > 0:
            driver.execute_script("arguments[0].click();", results[0])
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PYvSYb"))
            )

        # 설명 찾기
        try:
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PYvSYb"))
            )
            return description_element.text or ""
        except TimeoutException:
            return ""

    except TimeoutException:
        print(f"Timeout: {place_name}의 검색 과정에서 시간이 초과되었습니다.")
        return ""

    except Exception as e:
        print(f"전체 프로세스에서 예상치 못한 오류 발생: {e}")
        return ""

    finally:
        driver.quit()

