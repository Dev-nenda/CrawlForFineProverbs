from sqlalchemy import inspect
from database.db_connector import setup_database
from models.tables import Base, Sources, IntermediateTable, FinalResult, AuthorList


def create_tables():
    config_file_path = "config/mysql_config.txt"

    # MySQL 연결 설정 함수 호출
    engine, session, _ = setup_database(config_file_path)
    # 모든 테이블 생성

    inspector = inspect(engine)
    existing_table = inspector.get_table_names()

    tables_to_check = [
        Sources.__tablename__,
        IntermediateTable.__tablename__,
        FinalResult.__tablename__,
        AuthorList.__tablename__,
    ]

    for tablename in tables_to_check:
        if tablename in existing_table:
            print(f"{tablename} 테이블은 이미 존재합니다.")
        else:
            print(f"{tablename} 테이블은 존재하지 않습니다.")
            Base.metadata.tables[tablename].create(engine)

            print(f"{tablename} 테이블을 생성했습니다.")

    # 세션 종료
    session.close()


if __name__ == "__main__":
    create_tables()
