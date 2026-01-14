"""Configuration settings for Ground Stone bot."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "@GC_golf_audit_bot")

# DART API Configuration
DART_API_KEY = os.getenv("DART_API_KEY")
DART_BASE_URL = "https://opendart.fss.or.kr/api"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/ground-stone.db")

# Scheduler Configuration
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "60"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", f"{BASE_DIR}/logs/ground-stone.log")

# Industry Configuration
INDUSTRY_CODE = os.getenv("INDUSTRY_CODE", "91221")
INDUSTRY_NAME = os.getenv("INDUSTRY_NAME", "골프장 운영업")

# Report Types to Monitor
REPORT_TYPES = {
    "audit": "감사보고서",
    "business": "사업보고서",
    "semi_annual": "반기보고서",
    "quarterly": "분기보고서"
}


def validate_config():
    """Validate required configuration."""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")
    if not DART_API_KEY:
        raise ValueError("DART_API_KEY is required")

    # Create necessary directories
    data_dir = BASE_DIR / "data"
    logs_dir = BASE_DIR / "logs"
    data_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

    return True
