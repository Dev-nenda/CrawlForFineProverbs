from database.db_connector import setup_database
from crawlers.crawlers_url import Url
from crawlers.crawlers_data import CrawlModule

config_file_path = "config/mysql_config.txt"

# MySQL 연결 설정 함수 호출
engine, session, Base = setup_database(config_file_path)

url_processor = Url(engine)
crawl_module = CrawlModule(engine)

urls = url_processor.extract_urls()
print(urls)

for url in urls:
    is_active = url_processor.check_is_active(url)
    print(is_active)

    if is_active:
        crawl_module.crawl_url(url)
        crawl_module.close_driver()

url_processor.close_connection()
crawl_module.result_data.close_connection()
