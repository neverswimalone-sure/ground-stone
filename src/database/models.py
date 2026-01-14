"""Database models for Ground Stone."""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

Base = declarative_base()


class ProcessedReport(Base):
    """Model for tracking processed audit reports."""

    __tablename__ = "processed_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rcept_no = Column(String(20), unique=True, nullable=False, index=True)
    corp_code = Column(String(10), nullable=False)
    corp_name = Column(String(100), nullable=False)
    stock_code = Column(String(10))
    report_nm = Column(String(200), nullable=False)
    rcept_dt = Column(String(8), nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    notified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<ProcessedReport(corp_name='{self.corp_name}', report_nm='{self.report_nm}')>"


class MonitorLog(Base):
    """Model for logging monitoring activities."""

    __tablename__ = "monitor_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)  # success, error, warning
    message = Column(String(500))
    reports_found = Column(Integer, default=0)
    reports_notified = Column(Integer, default=0)

    def __repr__(self):
        return f"<MonitorLog(status='{self.status}', timestamp='{self.timestamp}')>"


# Database setup
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_database():
    """Initialize database and create tables."""
    Base.metadata.create_all(engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
