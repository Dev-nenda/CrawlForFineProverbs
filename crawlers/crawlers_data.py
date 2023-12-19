import ast
import time

from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from database.db_operations import Result_data
from database.db_connector import setup_database
from models.tables import Sources


# MySQL 설정 파일 경로
config_file_path = "config/mysql_config.txt"

# MySQL 연결 설정 함수 호출
engine, session, Base = setup_database(config_file_path)


class CrawlModule:
    def __init__(self, engine):
        # 클래스 초기화 작업 수행
        self.driver = None  # 웹 드라이버 초기화 등
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.result_data = Result_data(engine)

    def init_driver(self):
        # 웹 드라이버 초기화 작업 수행
        self.driver = webdriver.Chrome()

    def access_url(self, url):
        # URL에 접근하는 작업 수행
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            print(f"Error accessing URL: {e}")
            return False

    def click_element(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            element.click()
            time.sleep(1)  # 원하는 경우 대기 시간 조절
            return True
        except Exception as e:
            print(f"Failed to click element at XPath '{value}': {e}")
            return False

    def get_url_record(self, url):
        url_record = (
            self.session.query(Sources).filter(Sources.url == url).first()
        )  # sources 가 없으면 None

        return url_record

    def crawl_dynamic_chengyu_page_with_topic(self, url_record):
        """
        동적 고사성어 페이지 크롤링 함수
        """
        url = url_record.url
        topic_tag = url_record.topic_tag
        zh_tag = url_record.zh_tag
        kr_tag = url_record.kr_tag
        explanation_tag = url_record.explanation_tag
        class_type = url_record.class_type
        url_source = url_record.url_source
        page_tag = url_record.page_tag

        # 드라이버 초기화
        self.init_driver()

        if not self.access_url(url):
            return print("access 실패")  # url 접근 실패시 종료

        time.sleep(2)

        for div_index in range(1, 7):
            for li_index in range(1, 10):
                time.sleep(2)

                if div_index == 1 and li_index == 1:
                    continue  # 이 조합은 건너뜁니다.

                select_topic_xpath = f'//*[@id="content"]/div/div[2]/div[1]/div/div/div[{div_index}]/ul/li[{li_index}]/label'

                if topic_tag:
                    try:
                        self.click_element(By.XPATH, eval(f'f"""{topic_tag}"""'))

                        while True:
                            zh_elements = self.driver.find_elements(By.XPATH, zh_tag)

                            for zh_index, zh_element in enumerate(zh_elements):
                                kr_elements = self.driver.find_elements(
                                    By.XPATH, kr_tag
                                )

                                time.sleep(2)

                                zh_text = zh_element.text

                                # 인덱스로 인해 반복되는 kr_text 대신 kr_elements에서 해당 인덱스에 해당하는 요소를 직접 참조합니다.
                                kr_text = kr_elements[zh_index].text

                                topic_xpath_text = self.driver.find_element(
                                    By.XPATH, select_topic_xpath
                                ).text
                                explanation_text = (
                                    self.driver.find_element(
                                        By.XPATH, eval(f'f"""{explanation_tag}"""')
                                    )
                                    .text.replace("\n", "")
                                    .replace("\t", "")
                                )

                                self.result_data.save_crawling_data(
                                    {
                                        "category": topic_xpath_text,
                                        "type": class_type,
                                        "contents_kr": kr_text,
                                        "contents_eng": "",
                                        "contents_zh": zh_text,
                                        "contents_detail": explanation_text,
                                        "author": "",
                                        "url_name": url_source,
                                    }
                                )

                                print(f"{kr_text} is crawled")

                            if zh_index == len(zh_elements) - 1:
                                time.sleep(3)
                                try:
                                    self.driver.find_element(
                                        By.CSS_SELECTOR, page_tag
                                    ).click()

                                    print("다음페이지")

                                except NoSuchElementException:
                                    print("페이지가 없습니다.")
                                    break

                    except NoSuchElementException:
                        print("No More Topic")

    def crawl_dynamic_chengyu_page(self, url_record):
        """
        동적 고사성어 페이지 크롤링 함수
        """
        url = url_record.url
        zh_tag = url_record.zh_tag
        kr_tag = url_record.kr_tag
        explanation_tag = url_record.explanation_tag
        class_type = url_record.class_type
        url_source = url_record.url_source
        page_tag = url_record.page_tag

        # 드라이버 초기화
        self.init_driver()

        if not self.access_url(url):
            return print("access 실패")  # url 접근 실패시 종료

        time.sleep(2)

        while True:
            zh_elements = self.driver.find_elements(By.XPATH, zh_tag)

            for zh_index, zh_element in enumerate(zh_elements):
                kr_elements = self.driver.find_elements(By.XPATH, kr_tag)

                time.sleep(2)

                zh_text = zh_element.text

                # 인덱스로 인해 반복되는 kr_text 대신 kr_elements에서 해당 인덱스에 해당하는 요소를 직접 참조합니다.
                kr_text = kr_elements[zh_index].text

                explanation_text = (
                    self.driver.find_element(
                        By.XPATH, eval(f'f"""{explanation_tag}"""')
                    )
                    .text.replace("\n", "")
                    .replace("\t", "")
                )

                self.result_data.save_crawling_data(
                    {
                        "category": "",
                        "type": class_type,
                        "contents_kr": kr_text,
                        "contents_eng": "",
                        "contents_zh": zh_text,
                        "contents_detail": explanation_text,
                        "author": "",
                        "url_name": url_source,
                    }
                )

                print(f"{kr_text} is crawled")

            if zh_index == len(zh_elements) - 1:
                time.sleep(3)
                try:
                    self.driver.find_element(By.CSS_SELECTOR, page_tag).click()

                    print("다음페이지")

                except NoSuchElementException:
                    print("페이지가 없습니다.")
                    break

    def crawl_dynamic_quotation_page_with_topic(self, url_record):
        url = url_record.url
        class_type = url_record.class_type
        topic_tag = url_record.topic_tag
        kr_tag = url_record.kr_tag
        eng_tag = url_record.eng_tag
        author_tag = url_record.author_tag
        url_source = url_record.url_source

        self.init_driver()

        if not self.access_url(url):
            return print("access 실패")  # url 접근 실패시 종료

        print(f"Success access{url}")
        time.sleep(2)

        for topic_index in range(1, 13):
            self.click_element(
                By.XPATH,
                eval(f'f"""{topic_tag}"""'),
            )

            time.sleep(2)

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            # url_record['kr_tag']
            kr_tag = ast.literal_eval(f"({kr_tag})")
            kr_elements = soup.find_all(*kr_tag)

            eng_tag = ast.literal_eval(f"({eng_tag})")
            eng_elements = soup.find_all(*eng_tag)

            author_elements = soup.find_all(author_tag)
            print(author_tag)

            topic_xpath_text = self.driver.find_element(
                By.XPATH, eval(f'f"""{topic_tag}"""')
            ).text

            for index, kr_element in enumerate(kr_elements):
                print(index)
                kr_text = kr_element.text
                print(kr_text)
                eng_text = eng_elements[index].text
                print(eng_text)
                author_text = author_elements[index].text
                print(author_text)

                print(f"{kr_text} is crawled")

                self.result_data.save_crawling_data(
                    {
                        "category": topic_xpath_text,
                        "type": class_type,
                        "contents_kr": kr_text,
                        "contents_eng": eng_text,
                        "contents_zh": "",
                        "contents_detail": "",
                        "author": author_text,
                        "url_name": url_source,
                    }
                )

    def crawl_dynamic_quotation_page(self, url_record):
        url = url_record.url
        class_type = url_record.class_type
        kr_tag = url_record.kr_tag
        eng_tag = url_record.eng_tag
        author_tag = url_record.author_tag
        url_source = url_record.url_source

        self.init_driver()

        if not self.access_url(url):
            return print("access 실패")  # url 접근 실패시 종료

        print(f"Success access{url}")
        time.sleep(2)

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # url_record['kr_tag']
        kr_tag = ast.literal_eval(f"({kr_tag})")
        kr_elements = soup.find_all(*kr_tag)

        eng_tag = ast.literal_eval(f"({eng_tag})")
        eng_elements = soup.find_all(*eng_tag)

        author_elements = soup.find_all(author_tag)
        print(author_tag)

        for index, kr_element in enumerate(kr_elements):
            print(index)
            kr_text = kr_element.text
            print(kr_text)
            eng_text = eng_elements[index].text
            print(eng_text)
            author_text = author_elements[index].text
            print(author_text)

            print(f"{kr_text} is crawled")

            self.result_data.save_crawling_data(
                {
                    "category": "",
                    "type": class_type,
                    "contents_kr": kr_text,
                    "contents_eng": eng_text,
                    "contents_zh": "",
                    "contents_detail": "",
                    "author": author_text,
                    "url_name": url_source,
                }
            )

    def crawl_others(self, url_record):
        # 기타 타입 크롤링 코드
        url = url_record.url
        class_type = url_record.class_type
        start_index = url_record.start_index
        end_index = url_record.end_index
        all_tag = url_record.all_tag
        url_source = url_record.url_source

        self.init_driver()

        if not self.access_url(url):
            return print("access 실패")  # url 접근 실패시 종료

        print(f"Success access{url}")
        time.sleep(2)

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        if "," in all_tag:
            all_tag = ast.literal_eval(f"({all_tag})")
            all_elements = soup.find_all(*all_tag)
            print(*all_tag)
        else:
            all_elements = soup.find_all(all_tag)

        temporary_list = []

        for obj in all_elements[start_index:end_index]:
            temporary_list.append(obj.get_text())

        # 리스트에서 빈 값은 제거
        elements = [sentence for sentence in temporary_list if sentence.strip()]

        for element in elements:
            print(f"{element}is crawled")

            self.result_data.save_crawling_data(
                {
                    "type": class_type,
                    "contents_detail": element,
                    "url_name": url_source,
                }
            )

    def crawl_url(self, url):
        url_record = self.get_url_record(url)

        url_type = url_record.url_type
        class_type = url_record.class_type
        topic_tag = url_record.topic_tag

        if url_type == 1 and class_type == 1:  # 성어
            if topic_tag:
                self.crawl_dynamic_chengyu_page_with_topic(url_record)
            else:
                self.crawl_dynamic_chengyu_page(url_record)

        elif url_type == 1 and class_type == 0:  # 명언
            if topic_tag:
                self.crawl_dynamic_quotation_page_with_topic(url_record)
            else:
                self.crawl_dynamic_quotation_page(url_record)

        elif url_type == 0 and class_type == 0:
            self.crawl_others(url_record)

    def close_driver(self):
        # 웹 드라이버 종료 작업 수행
        if self.driver:
            self.driver.quit()
