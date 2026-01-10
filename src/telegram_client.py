"""
텔레그램 알림 클라이언트 모듈
"""

import requests
import logging
from typing import Optional, Any, List
from datetime import datetime

from .config import config

logger = logging.getLogger(__name__)


class TelegramClient:
    """텔레그램 봇 클라이언트 클래스"""

    def __init__(
        self,
        bot_token: str = config.TELEGRAM_BOT_TOKEN,
        chat_id: str = config.TELEGRAM_CHAT_ID
    ):
        """
        Args:
            bot_token: 텔레그램 봇 토큰
            chat_id: 메시지를 보낼 채팅 ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"{config.TELEGRAM_API_BASE_URL}/bot{bot_token}"

    def send_message(
        self,
        text: str,
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True
    ) -> bool:
        """
        텔레그램 메시지 전송

        Args:
            text: 전송할 메시지 텍스트
            parse_mode: 메시지 파싱 모드 (HTML, Markdown 등)
            disable_web_page_preview: 링크 미리보기 비활성화 여부

        Returns:
            전송 성공 여부
        """
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            if result.get("ok"):
                logger.info("텔레그램 메시지 전송 성공")
                return True
            else:
                logger.error(f"텔레그램 메시지 전송 실패: {result.get('description')}")
                return False

        except requests.RequestException as e:
            logger.error(f"텔레그램 API 호출 실패: {e}")
            return False

    def send_audit_report_notification(self, disclosure: Any) -> bool:
        """
        감사보고서 공시 알림 메시지 전송

        Args:
            disclosure: DartDisclosure 객체

        Returns:
            전송 성공 여부
        """
        # 날짜 포맷팅 (YYYYMMDD -> YYYY-MM-DD)
        rcept_dt_formatted = "-".join([
            disclosure.rcept_dt[:4],
            disclosure.rcept_dt[4:6],
            disclosure.rcept_dt[6:8]
        ])

        # HTML 형식 메시지 작성
        message = f"""🏌️ <b>[DART 감사보고서 알림]</b>

<b>회사명:</b> {disclosure.corp_name}
<b>고유번호:</b> {disclosure.corp_code}
<b>보고서명:</b> {disclosure.report_nm}
<b>접수번호:</b> {disclosure.rcept_no}
<b>공시일자:</b> {rcept_dt_formatted}

🔗 <a href="{disclosure.detail_url}">공시 상세보기</a>

<i>알림 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"""

        return self.send_message(message)

    def send_summary_notification(
        self,
        total_companies: int,
        new_reports_count: int,
        reports: list
    ) -> bool:
        """
        모니터링 요약 알림 전송

        Args:
            total_companies: 전체 모니터링 회사 수
            new_reports_count: 신규 발견된 감사보고서 수
            reports: 신규 감사보고서 목록

        Returns:
            전송 성공 여부
        """
        if new_reports_count == 0:
            message = f"""📊 <b>[DART 모니터링 요약]</b>

모니터링 회사: {total_companies}개
신규 감사보고서: <b>없음</b>

<i>실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"""
        else:
            reports_list = "\n".join([
                f"  • {r.corp_name} - {r.report_nm}"
                for r in reports[:10]  # 최대 10개만 표시
            ])

            more_text = ""
            if new_reports_count > 10:
                more_text = f"\n  ... 외 {new_reports_count - 10}건"

            message = f"""📊 <b>[DART 모니터링 요약]</b>

모니터링 회사: {total_companies}개
신규 감사보고서: <b>{new_reports_count}건</b>

<b>신규 공시 목록:</b>
{reports_list}{more_text}

<i>실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"""

        return self.send_message(message)

    def test_connection(self) -> bool:
        """
        텔레그램 봇 연결 테스트

        Returns:
            연결 성공 여부
        """
        test_message = f"""✅ <b>DART 모니터링 봇 연결 테스트</b>

텔레그램 연동이 정상적으로 작동합니다.

<i>테스트 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"""

        return self.send_message(test_message)


if __name__ == "__main__":
    # 테스트 코드
    logging.basicConfig(level=logging.INFO)

    client = TelegramClient()

    # 연결 테스트
    print("텔레그램 연결 테스트 중...")
    if client.test_connection():
        print("✅ 연결 성공!")
    else:
        print("❌ 연결 실패!")
