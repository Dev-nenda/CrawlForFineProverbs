from sqlalchemy.orm import sessionmaker
from database.db_connector import setup_database
from models.tables import Sources, IntermediateTable

# MySQL 설정 파일 경로
config_file_path = "config/mysql_config.txt"

# MySQL 연결 설정 함수 호출
engine, session, Base = setup_database(config_file_path)


class Source_data:
    def __init__(self, engine):
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_field_values(self):
        records = self.session.query(Sources).all()
        if records:
            field_values = [
                (
                    record.id,
                    record.url_type,
                    record.class_type,
                    record.url,
                    record.url_source,
                    record.topic_tag,
                    record.page_tag,
                    record.kr_tag,
                    record.eng_tag,
                    record.zh_tag,
                    record.explanation_tag,
                    record.author_tag,
                    record.start_index,
                    record.end_index,
                    record.all_tag,
                    record.is_active,
                )
                for record in records
            ]
            return field_values
        else:
            return []

    def close_connection(self):
        self.session.close()


class Result_data:
    def __init__(self, engine):
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_crawling_data(self, data):
        new_data = IntermediateTable(
            category=data.get("category", None),
            type=data.get("type", 0),
            contents_kr=data.get("contents_kr", None),
            contents_eng=data.get("contents_eng", None),
            contents_zh=data.get("contents_zh", None),
            contents_detail=data.get("contents_detail", None),
            author=data.get("author", None),
            url_name=data.get("url_name", None),
        )
        self.session.add(new_data)
        self.session.commit()

    def close_connection(self):
        self.session.close()
