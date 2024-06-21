# 定义小说模型
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float

Base = declarative_base()
class Novel(Base):
    __tablename__ = 'novels_collect'

    id = Column(String(255), primary_key=True)  # 将 id 字段类型改为 String
    title = Column(String(255))
    authors = Column(String(255))
    brief = Column(Text)
    categories = Column(String(255))
    tags = Column(String(255))
    wordCount = Column(Integer)
    pornRate = Column(Float)
    collectCount = Column(Integer)
    latestUpdate = Column(String(255))
    updateTime = Column(DateTime)
    createTime = Column(DateTime)  # 添加 createTime 字段