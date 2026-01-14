"""Main entry point for Ground Stone bot."""
import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import validate_config, LOG_LEVEL, LOG_FILE
from src.database.models import init_database
from src.scheduler.tasks import MonitorService
from src.bot.notifications import NotificationService

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def test_connections():
    """Test connections to DART and Telegram."""
    logger.info("Testing connections...")

    # Test Telegram connection
    notification_service = NotificationService()
    telegram_ok = await notification_service.test_connection()

    if not telegram_ok:
        logger.error("Telegram connection test failed")
        return False

    logger.info("All connection tests passed")
    return True


async def main():
    """Main function to run the bot."""
    logger.info("=" * 50)
    logger.info("Ground Stone - Golf Course Audit Report Monitor")
    logger.info("=" * 50)

    try:
        # Validate configuration
        logger.info("Validating configuration...")
        validate_config()

        # Initialize database
        logger.info("Initializing database...")
        init_database()

        # Test connections
        if not await test_connections():
            logger.error("Connection tests failed. Please check your configuration.")
            return

        # Initialize and start monitor service
        logger.info("Starting monitor service...")
        monitor = MonitorService()

        # Run initial check
        await monitor.run_manual_check()

        # Start scheduler
        monitor.start()

        # Keep the program running
        logger.info("Bot is now running. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return

    finally:
        logger.info("Shutting down...")
        if 'monitor' in locals():
            monitor.stop()
        logger.info("Shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
