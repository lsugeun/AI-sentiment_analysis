from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import csv

# ChromeDriver 경로 설정
chrome_driver_path = 'chromedriver.exe'  # 'chromedriver.exe' 파일의 경로로 설정하세요.

# Chrome 옵션 설정 (선택 사항)
chrome_options = Options()
chrome_options.add_argument('--headless')  # 헤드리스 모드로 실행하려면 이 옵션을 추가

# Chrome WebDriver 초기화
driver = WebDriver(service=Service(chrome_driver_path), options=chrome_options)

# 웹 페이지 열기
driver.get("https://n.news.naver.com/mnews/article/comment/025/0003308866?sid=103")
time.sleep(5)  # 페이지 로딩 대기

comment_count = 0  # 댓글 개수를 추적

csv_data = []  # 댓글을 저장할 리스트

try:
    while comment_count < 50:  # 댓글 개수가 50개 미만인 동안 실행
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, "span.u_cbox_page_more")
            ActionChains(driver).move_to_element(load_more_button).click(load_more_button).perform()
            time.sleep(3)  # 새로운 댓글 로딩 대기
        except Exception as e:
            print("더 이상 불러올 댓글이 없습니다.")
            break

        # 댓글 추출
        comments = driver.find_elements(By.CLASS_NAME, "u_cbox_comment")
        comment_count = len(comments)  # 댓글 개수 업데이트

except Exception as e:
    print("예상치 못한 오류가 발생했습니다.")

finally:
    # 댓글 추출 (최대 50개)
    comments = driver.find_elements(By.CLASS_NAME, "u_cbox_comment")[:50]
    for i, comment in enumerate(comments):
        try:
            comment_text = comment.find_element(By.CLASS_NAME, "u_cbox_contents").text
            print(f"{i+1}. 댓글: {comment_text}")
            csv_data.append([i+1, comment_text])
        except Exception as e:
            pass  # 실패한 경우 아무 것도 하지 않음

    driver.quit()  # 드라이버 종료

    # CSV 파일로 저장
    with open('comments.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Comment'])  # 헤더 추가
        writer.writerows(csv_data)  # 데이터 추가