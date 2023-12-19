from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sources(Base):
    """
    크롤링 Url 대상 tag들을 입력한 source table을 정의
    """

    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url_type = Column(Integer, nullable=False, default=0)  # 기본값 0 (정적 페이지)
    class_type = Column(Integer, nullable=False, default=0)  # 기본값 0 (명언 페이지)
    url = Column(String(600), nullable=False)
    url_source = Column(String(600), nullable=False)
    topic_tag = Column(String(600), nullable=True)
    page_tag = Column(String(600), nullable=True)
    kr_tag = Column(String(600), nullable=True)
    eng_tag = Column(String(600), nullable=True)
    zh_tag = Column(String(600), nullable=True)
    explanation_tag = Column(String(600), nullable=True)
    author_tag = Column(String(600), nullable=True)
    start_index = Column(Integer, nullable=True)
    end_index = Column(Integer, nullable=True)
    all_tag = Column(String(600), nullable=True)
    is_active = Column(Boolean, default=True)


class IntermediateTable(Base):
    """
    크롤링 실행 후 raw 데이터를 저장하는 중간 table을 정의
    """

    __tablename__ = "intermediate_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(500), nullable=True)
    type = Column(Integer, nullable=False, default=0)
    url_name = Column(String(600), nullable=False)
    contents_kr = Column(String(600), nullable=True)
    contents_eng = Column(String(600), nullable=True)
    contents_zh = Column(String(600), nullable=True)
    contents_detail = Column(String(600), nullable=True)
    author = Column(String(600), nullable=True)
    crawled_at = Column(DateTime, server_default=func.now())


class FinalResult(Base):
    __tablename__ = "final_result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(500), nullable=True)
    type = Column(Integer, nullable=False, default=0)  # 기본값 0 (명언 페이지)
    url_name = Column(String(600), nullable=False)
    contents_kr = Column(String(600), nullable=True)
    contents_eng = Column(String(600), nullable=True)
    contents_zh = Column(String(600), nullable=True)
    contents_detail = Column(String(600), nullable=True)
    contents_divided = Column(String(600), nullable=True)
    author = Column(String(600), nullable=True)
    continent = Column(String(600), nullable=True)
    crawled_at = Column(DateTime, server_default=func.now())


class AuthorList(Base):
    __tablename__ = "authorlist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(600), nullable=False)
    continent = Column(String(600), nullable=False)
