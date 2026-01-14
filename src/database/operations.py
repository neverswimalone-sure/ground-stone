"""Database operations for Ground Stone."""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from .models import ProcessedReport, MonitorLog

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations."""

    def __init__(self, db_session: Session):
        """Initialize database service with session."""
        self.db = db_session

    def is_report_processed(self, rcept_no: str) -> bool:
        """
        Check if a report has already been processed.

        Args:
            rcept_no: Receipt number of the report

        Returns:
            True if report exists, False otherwise
        """
        report = self.db.query(ProcessedReport).filter(
            ProcessedReport.rcept_no == rcept_no
        ).first()
        return report is not None

    def add_processed_report(self, report_data: dict) -> ProcessedReport:
        """
        Add a processed report to the database.

        Args:
            report_data: Dictionary containing report information

        Returns:
            ProcessedReport instance
        """
        report = ProcessedReport(
            rcept_no=report_data.get("rcept_no"),
            corp_code=report_data.get("corp_code"),
            corp_name=report_data.get("corp_name"),
            stock_code=report_data.get("stock_code"),
            report_nm=report_data.get("report_nm"),
            rcept_dt=report_data.get("rcept_dt"),
            notified=True
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        logger.info(f"Added processed report: {report.corp_name}")
        return report

    def get_recent_reports(self, limit: int = 10) -> List[ProcessedReport]:
        """
        Get recent processed reports.

        Args:
            limit: Maximum number of reports to return

        Returns:
            List of ProcessedReport instances
        """
        reports = self.db.query(ProcessedReport).order_by(
            ProcessedReport.processed_at.desc()
        ).limit(limit).all()

        return reports

    def add_monitor_log(
        self,
        status: str,
        message: str,
        reports_found: int = 0,
        reports_notified: int = 0
    ) -> MonitorLog:
        """
        Add a monitoring log entry.

        Args:
            status: Status of the monitoring run
            message: Log message
            reports_found: Number of reports found
            reports_notified: Number of reports notified

        Returns:
            MonitorLog instance
        """
        log = MonitorLog(
            status=status,
            message=message,
            reports_found=reports_found,
            reports_notified=reports_notified
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log

    def get_recent_logs(self, limit: int = 20) -> List[MonitorLog]:
        """
        Get recent monitor logs.

        Args:
            limit: Maximum number of logs to return

        Returns:
            List of MonitorLog instances
        """
        logs = self.db.query(MonitorLog).order_by(
            MonitorLog.timestamp.desc()
        ).limit(limit).all()

        return logs

    def get_statistics(self) -> dict:
        """
        Get statistics about processed reports.

        Returns:
            Dictionary containing statistics
        """
        total_reports = self.db.query(ProcessedReport).count()
        total_companies = self.db.query(ProcessedReport.corp_code).distinct().count()

        return {
            "total_reports": total_reports,
            "total_companies": total_companies,
            "last_updated": datetime.utcnow().isoformat()
        }
