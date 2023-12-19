from sqlalchemy.orm import sessionmaker
from database.db_connector import setup_database
from models.tables import Sources

# MySQL 설정 파일 경로
config_file_path = "config/mysql_config.txt"

# MySQL 연결 설정 함수 호출
engine, session, Base = setup_database(config_file_path)


class Url:
    """
    sources 테이블에 저장되어있는 url과 관련된 기능을 담아둔 클래스
    """

    def __init__(self, engine):
        self.engine = engine
        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    def extract_urls(self):
        """
        테이블에서 url 목록을 추출하여 리스트로 반환하는 함수
        """

        # sources table에 저장된 url 목록들을 모두 가져오기.
        records = self.session.query(Sources.url).all()

        # 가져온 url들을 리스트로 변환, url 값이 없을 경우 공백으로 반환
        url_list = [record[0] for record in records] if records else []

        # url 리스트 반환
        return url_list

    def check_is_active(self, url):
        """
        해당 url의 is_active 값이 True인지 확인하고, 찾을 수 없을 경우 기본적으로 False 반환합니다.
        """
        # URL에 해당하는 is_active 값을 데이터베이스에서 가져옵니다.
        record = (
            self.session.query(Sources.is_active).filter(Sources.url == url).first()
        )

        # URL을 찾을 경우 해당 is_active 값을 반환하고, 찾을 수 없는 경우 기본적으로 False를 반환합니다.
        return record[0] if record else False

    def close_connection(self):
        self.session.close()
