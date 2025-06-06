from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from src.configure.database import Base, engine

class SortUrls(Base):
    __tablename__ = "ulrs"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False, unique=True)
    short_url = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)


class Clicks(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    sort_url_id = Column(Integer, ForeignKey("ulrs.id"), nullable=False)
    click_count = Column(Integer, default=0)
    last_clicked_at = Column(DateTime, nullable=True)


Base.metadata.create_all(bind=engine)