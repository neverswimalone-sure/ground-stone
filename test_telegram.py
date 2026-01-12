#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
텔레그램 봇 연결 테스트
"""

import requests

# 텔레그램 설정
TELEGRAM_BOT_TOKEN = "8180938946:AAHgoRR7Tt_3J_gyENJXt32qGa0kJ5nQxGM"
TELEGRAM_CHAT_ID = "143110040"

def test_telegram():
    """텔레그램 연결 테스트"""

    # 테스트 메시지
    message = """🏌️ 골프 딜 뉴스 봇 - 연결 테스트

✅ 텔레그램 봇이 정상적으로 작동하고 있습니다!

📋 봇 설정:
- 24시간 이내 뉴스만 수집
- 평일 9시~18시, 30분마다 자동 실행
- 제목 + 링크 간결한 포맷

🔗 테스트 링크 예시:
https://example.com/golf-deal-news"""

    # 텔레그램 API URL
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # 전송할 데이터
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'disable_web_page_preview': False
    }

    try:
        print("📤 텔레그램 연결 테스트 중...")
        response = requests.post(url, data=payload, timeout=10)

        if response.status_code == 200:
            print("✅ 성공! 텔레그램으로 메시지가 전송되었습니다.")
            print(f"   └─ 응답 코드: {response.status_code}")
            return True
        else:
            print(f"❌ 실패! 응답 코드: {response.status_code}")
            print(f"   └─ 응답 내용: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return False

if __name__ == "__main__":
    test_telegram()
