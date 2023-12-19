# db_connector.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql


def setup_database(file_path):
    # file_path에 저장되어 있는 config 파일 가져오기
    config = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=")
                config[key] = value

    # MySQL 연결 정보 가져오기
    user = config.get("MYSQL_USER")
    password = config.get("MYSQL_PASSWORD")
    host = config.get("MYSQL_HOST")
    port = config.get("MYSQL_PORT")
    database = config.get("MYSQL_DATABASE")

    # MySQL 연결 설정
    db_config = {"host": host, "user": user, "password": password}

    # MySQL 연결
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 데이터베이스 생성 SQL 실행
    create_db_sql = f"CREATE DATABASE IF NOT EXISTS {database};"
    cursor.execute(create_db_sql)

    # 연결 및 커서 닫기
    cursor.close()
    conn.close()

    # SQLAlchemy engine, session, base 생성
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}", echo=True
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()

    return engine, session, Base


# # 다른 Python 파일에서 db_connector.py 파일의 함수를 import
# from db_connector import setup_database

# # MySQL 설정 파일 경로
# config_file_path = "config/mysql_config.txt"

# # MySQL 연결 설정 함수 호출
# engine, session, Base = setup_database(config_file_path)

# # 이후 engine, session, Base를 이용하여 원하는 작업 수행
# # 예: SQLAlchemy ORM을 사용하여 데이터베이스 작업 수행
