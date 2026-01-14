"""Scheduled tasks for monitoring audit reports."""
import logging
import asyncio
from typing import List, Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

from src.dart.client import DARTClient
from src.bot.notifications import NotificationService
from src.database.models import SessionLocal
from src.database.operations import DatabaseService
from config.settings import CHECK_INTERVAL_MINUTES

logger = logging.getLogger(__name__)


class MonitorService:
    """Service for monitoring and processing audit reports."""

    def __init__(self):
        """Initialize monitor service."""
        self.dart_client = DARTClient()
        self.notification_service = NotificationService()
        self.scheduler = AsyncIOScheduler()

    async def process_new_reports(self, reports: List[Dict]) -> int:
        """
        Process new audit reports and send notifications.

        Args:
            reports: List of report dictionaries

        Returns:
            Number of reports processed and notified
        """
        notified_count = 0
        db = SessionLocal()
        db_service = DatabaseService(db)

        try:
            for report in reports:
                rcept_no = report.get("rcept_no")

                # Check if already processed
                if db_service.is_report_processed(rcept_no):
                    logger.debug(f"Report {rcept_no} already processed, skipping")
                    continue

                # Send notification
                success = await self.notification_service.send_notification(report)

                if success:
                    # Save to database
                    db_service.add_processed_report(report)
                    notified_count += 1
                    logger.info(f"Processed and notified: {report.get('corp_name')}")
                else:
                    logger.warning(f"Failed to notify: {report.get('corp_name')}")

            return notified_count

        finally:
            db.close()

    async def check_for_reports(self):
        """Check for new audit reports and process them."""
        logger.info("Starting scheduled check for new reports...")

        db = SessionLocal()
        db_service = DatabaseService(db)

        try:
            # Fetch recent audit reports
            reports = self.dart_client.get_recent_audit_reports(days=1)

            logger.info(f"Found {len(reports)} audit reports")

            # Process new reports
            notified_count = await self.process_new_reports(reports)

            # Log the monitoring activity
            db_service.add_monitor_log(
                status="success",
                message=f"Check completed successfully",
                reports_found=len(reports),
                reports_notified=notified_count
            )

            logger.info(f"Check completed: {notified_count} new reports notified")

        except Exception as e:
            logger.error(f"Error during scheduled check: {e}")

            # Log the error
            db_service.add_monitor_log(
                status="error",
                message=f"Error: {str(e)}",
                reports_found=0,
                reports_notified=0
            )

        finally:
            db.close()

    def start(self):
        """Start the monitoring scheduler."""
        logger.info(f"Starting monitor service (check interval: {CHECK_INTERVAL_MINUTES} minutes)")

        # Add scheduled job
        self.scheduler.add_job(
            self.check_for_reports,
            trigger=IntervalTrigger(minutes=CHECK_INTERVAL_MINUTES),
            id="check_reports",
            name="Check for new audit reports",
            replace_existing=True
        )

        # Start scheduler
        self.scheduler.start()
        logger.info("Monitor service started")

    def stop(self):
        """Stop the monitoring scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Monitor service stopped")

    async def run_manual_check(self):
        """Run a manual check immediately."""
        logger.info("Running manual check...")
        await self.check_for_reports()
