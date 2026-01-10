"""
환경 변수 및 설정 관리 모듈
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """애플리케이션 설정 클래스"""

    # 프로젝트 루트 디렉토리
    ROOT_DIR = Path(__file__).parent.parent

    # 엑셀 파일 경로
    EXCEL_FILE_PATH = ROOT_DIR / "기업개황_20260110.xlsx"

    # 상태 저장 파일 경로
    STATE_FILE_PATH = ROOT_DIR / "state.json"

    # DART API 설정
    DART_API_KEY: str = os.getenv("DART_API_KEY", "")
    DART_API_BASE_URL = "https://opendart.fss.or.kr/api"

    # 텔레그램 설정
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    TELEGRAM_API_BASE_URL = "https://api.telegram.org"

    # 모니터링 설정
    TARGET_YEAR = 2025  # 모니터링 대상 연도
    TARGET_INDUSTRY = "골프장 운영업"  # 대상 업종

    # API 호출 딜레이 (초)
    API_DELAY = 0.5

    @classmethod
    def validate(cls) -> bool:
        """필수 환경 변수가 설정되어 있는지 확인"""
        if not cls.DART_API_KEY:
            raise ValueError("DART_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN이 설정되지 않았습니다. .env 파일을 확인하세요.")
        if not cls.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID가 설정되지 않았습니다. .env 파일을 확인하세요.")
        if not cls.EXCEL_FILE_PATH.exists():
            raise FileNotFoundError(f"엑셀 파일을 찾을 수 없습니다: {cls.EXCEL_FILE_PATH}")
        return True


config = Config()
