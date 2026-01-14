"""Test script to fetch and notify all 2025 golf course audit reports."""
import asyncio
import logging
import sys
from datetime import datetime

# Add src to path
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import validate_config, LOG_LEVEL
from src.dart.client import DARTClient
from src.bot.notifications import NotificationService
from src.database.models import init_database, SessionLocal
from src.database.operations import DatabaseService

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


async def test_2025_audit_reports():
    """Fetch and notify all golf course audit reports from 2025."""

    logger.info("=" * 80)
    logger.info("2025 Golf Course Audit Reports - Historical Test")
    logger.info("=" * 80)

    try:
        # Validate configuration
        logger.info("Validating configuration...")
        validate_config()

        # Initialize database
        logger.info("Initializing database...")
        init_database()

        # Initialize clients
        dart_client = DARTClient()
        notification_service = NotificationService()

        # Test Telegram connection
        logger.info("Testing Telegram connection...")
        telegram_ok = await notification_service.test_connection()

        if not telegram_ok:
            logger.error("Telegram connection test failed!")
            return

        logger.info("✅ Telegram connection successful!")

        # Get golf course companies
        logger.info("\nFetching golf course company list...")
        golf_companies = dart_client.get_golf_companies()

        if not golf_companies:
            logger.error("No golf course companies found!")
            return

        logger.info(f"✅ Found {len(golf_companies)} golf course companies")
        logger.info(f"Sample companies: {list(golf_companies.values())[:3]}")

        # Fetch 2025 disclosures
        logger.info("\n" + "=" * 80)
        logger.info("Fetching ALL disclosures from 2025-01-01 to 2025-12-31")
        logger.info("This may take a while...")
        logger.info("=" * 80 + "\n")

        start_date = "20250101"
        end_date = "20251231"

        result = dart_client.get_disclosure_list(start_date, end_date, page_count=100)
        all_disclosures = result.get("list", [])

        logger.info(f"✅ Fetched {len(all_disclosures)} total disclosures from 2025")

        # Filter for audit reports
        audit_reports = dart_client.filter_audit_reports(all_disclosures)
        logger.info(f"✅ Found {len(audit_reports)} audit reports (all companies)")

        # Filter for golf course companies only
        golf_audit_reports = []
        for report in audit_reports:
            corp_code = report.get("corp_code")
            if corp_code in golf_companies:
                report["induty_code"] = golf_companies[corp_code].get("induty_code", "")
                golf_audit_reports.append(report)

        logger.info(f"\n🎯 Found {len(golf_audit_reports)} golf course audit reports!")
        logger.info(f"Expected: 400-470 reports")

        if len(golf_audit_reports) < 400 or len(golf_audit_reports) > 470:
            logger.warning(f"⚠️  Count is outside expected range!")
        else:
            logger.info(f"✅ Count is within expected range!")

        # Show sample reports
        logger.info("\n📋 Sample golf course audit reports:")
        for i, report in enumerate(golf_audit_reports[:5], 1):
            logger.info(f"{i}. {report.get('corp_name')} - {report.get('report_nm')} - {report.get('rcept_dt')}")

        # Ask for confirmation before sending
        logger.info("\n" + "=" * 80)
        logger.info(f"⚠️  READY TO SEND {len(golf_audit_reports)} NOTIFICATIONS TO TELEGRAM")
        logger.info("=" * 80)
        logger.info(f"This will:")
        logger.info(f"  - Send {len(golf_audit_reports)} messages to your Telegram channel")
        logger.info(f"  - Take approximately {len(golf_audit_reports) / 30:.1f} seconds (rate limit)")
        logger.info(f"  - Save all reports to database")

        response = input("\n👉 Do you want to proceed? (yes/no): ")

        if response.lower() not in ['yes', 'y']:
            logger.info("❌ Test cancelled by user")
            return

        # Send notifications
        logger.info("\n📤 Starting to send notifications...")
        logger.info("=" * 80)

        db = SessionLocal()
        db_service = DatabaseService(db)

        sent_count = 0
        failed_count = 0

        try:
            for i, report in enumerate(golf_audit_reports, 1):
                rcept_no = report.get("rcept_no")

                # Check if already processed
                if db_service.is_report_processed(rcept_no):
                    logger.debug(f"[{i}/{len(golf_audit_reports)}] Skipping (already processed): {report.get('corp_name')}")
                    continue

                # Send notification
                logger.info(f"[{i}/{len(golf_audit_reports)}] Sending: {report.get('corp_name')} - {report.get('rcept_dt')}")

                success = await notification_service.send_notification(report)

                if success:
                    # Save to database
                    db_service.add_processed_report(report)
                    sent_count += 1
                    logger.info(f"✅ Sent successfully ({sent_count} total)")
                else:
                    failed_count += 1
                    logger.warning(f"❌ Failed to send ({failed_count} failed)")

                # Rate limiting: wait 0.1 seconds between messages (max 10/sec, well below 30/sec limit)
                await asyncio.sleep(0.1)

                # Progress update every 50 messages
                if i % 50 == 0:
                    logger.info(f"\n📊 Progress: {i}/{len(golf_audit_reports)} ({i/len(golf_audit_reports)*100:.1f}%)")
                    logger.info(f"   Sent: {sent_count}, Failed: {failed_count}\n")

        finally:
            db.close()

        # Final summary
        logger.info("\n" + "=" * 80)
        logger.info("🎉 TEST COMPLETED!")
        logger.info("=" * 80)
        logger.info(f"Total reports found: {len(golf_audit_reports)}")
        logger.info(f"Successfully sent: {sent_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Already processed: {len(golf_audit_reports) - sent_count - failed_count}")
        logger.info("=" * 80)

        # Add monitoring log
        db = SessionLocal()
        db_service = DatabaseService(db)
        try:
            db_service.add_monitor_log(
                status="success",
                message=f"Historical test: 2025 golf course audit reports",
                reports_found=len(golf_audit_reports),
                reports_notified=sent_count
            )
        finally:
            db.close()

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return


if __name__ == "__main__":
    try:
        asyncio.run(test_2025_audit_reports())
    except KeyboardInterrupt:
        logger.info("\n⚠️  Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
