from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'

# Desired Capabilities 설정
options = UiAutomator2Options()
options.platform_name = 'Android'
options.platform_version = '13'  # 실제 Android 버전으로 변경
options.device_name = "R39N400T11A"  # 실제 장치 이름으로 변경
options.app_package = 'com.samsung.android.calendar'
options.app_activity = 'com.samsung.android.app.calendar.activity.MainActivity'
options.automation_name = 'UiAutomator2'
options.no_reset = True  # 앱이 이미 설치되어 있고 초기화를 원치 않는 경우

# Appium 서버와 연결 시도
try:
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    print("Successfully connected to Appium server")
    # 대기 객체 생성
    wait = WebDriverWait(driver, 30)

    # "+" 버튼 클릭하여 새 일정 추가
    add_event_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "com.samsung.android.calendar:id/floating_action_button"))
    )
    add_event_btn.click()

    # 일정 제목 입력
    event_title_field = wait.until(
        EC.presence_of_element_located((By.ID, "com.samsung.android.calendar:id/title"))
    )
    event_title_field.send_keys("빼빼로 데이")

    start_time_field = driver.find_element(By.ID, "com.samsung.android.calendar:id/start_time")
    end_time_field = driver.find_element(By.ID, "com.samsung.android.calendar:id/end_time")
    start_time_field.click()

    driver.find_element(By.XPATH, "//android.widget.TextView[@text='11']").click()
    driver.find_element(By.XPATH, "//android.widget.TextView[@text='2024']").click()

    driver.find_element(By.XPATH, "//android.widget.TextView[@text='09:00']").click()
    end_time_field.click()
    driver.find_element(By.XPATH, "//android.widget.TextView[@text='05:00']").click()

    date_picker = driver.find_element(By.ID, "com.samsung.android.calendar:id/date_picker")
    date_picker.click()
    save_button = driver.find_element(By.ID, "com.samsung.android.calendar:id/save_button")
    save_button.click()
except Exception as e:
    print(f"Error connecting to Appium server: {e}")

