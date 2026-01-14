"""Telegram notification formatting and sending."""
import logging
from typing import Dict
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications to Telegram channel."""

    def __init__(self, bot_token: str = TELEGRAM_BOT_TOKEN, channel_id: str = TELEGRAM_CHANNEL_ID):
        """Initialize notification service."""
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id

    def format_audit_report_message(self, report: Dict) -> str:
        """
        Format audit report data into a readable message.

        Args:
            report: Dictionary containing report information

        Returns:
            Formatted message string
        """
        corp_name = report.get("corp_name", "N/A")
        corp_code = report.get("corp_code", "N/A")
        stock_code = report.get("stock_code", "N/A")
        report_nm = report.get("report_nm", "N/A")
        rcept_no = report.get("rcept_no", "")
        rcept_dt = report.get("rcept_dt", "")

        # Format date
        if rcept_dt and len(rcept_dt) == 8:
            try:
                date_obj = datetime.strptime(rcept_dt, "%Y%m%d")
                formatted_date = date_obj.strftime("%Y년 %m월 %d일")
            except ValueError:
                formatted_date = rcept_dt
        else:
            formatted_date = rcept_dt

        # Generate DART URL
        dart_url = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"

        message = f"""🏌️ **새로운 감사보고서가 제출되었습니다!**

📋 **회사명**: {corp_name}
🏢 **종목코드**: {stock_code if stock_code else corp_code}
📊 **보고서**: {report_nm}
📅 **제출일**: {formatted_date}
🔗 **링크**: [DART 바로가기]({dart_url})

💼 **업종**: 골프장 운영업
"""
        return message

    async def send_notification(self, report: Dict) -> bool:
        """
        Send notification about audit report to Telegram channel.

        Args:
            report: Dictionary containing report information

        Returns:
            True if successful, False otherwise
        """
        try:
            message = self.format_audit_report_message(report)

            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )

            logger.info(f"Sent notification for {report.get('corp_name')}")
            return True

        except TelegramError as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    async def send_status_message(self, message: str) -> bool:
        """
        Send a status message to the channel.

        Args:
            message: Status message to send

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="Markdown"
            )
            logger.info("Sent status message")
            return True

        except TelegramError as e:
            logger.error(f"Failed to send status message: {e}")
            return False

    async def test_connection(self) -> bool:
        """
        Test connection to Telegram bot and channel.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test bot connection
            bot_info = await self.bot.get_me()
            logger.info(f"Connected to bot: {bot_info.username}")

            # Test sending message
            test_message = "✅ Ground Stone 봇이 정상적으로 연결되었습니다."
            await self.send_status_message(test_message)

            return True

        except TelegramError as e:
            logger.error(f"Connection test failed: {e}")
            return False
