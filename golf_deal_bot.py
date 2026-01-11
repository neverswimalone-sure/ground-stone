#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
골프장 투자 및 M&A 뉴스 자동 수집 텔레그램 봇
작성일: 2026-01-10
"""

import requests  # HTTP 요청을 위한 라이브러리 (텔레그램 API 호출 및 RSS 가져오기)
import time  # 시간 관련 함수를 위한 라이브러리
from datetime import datetime, timedelta, timezone  # 날짜/시간 계산을 위한 라이브러리
from urllib.parse import quote  # URL 인코딩을 위한 함수
import hashlib  # 중복 체크를 위한 해시 생성
import xml.etree.ElementTree as ET  # XML 파싱을 위한 표준 라이브러리 (RSS 파싱용)
from email.utils import parsedate_to_datetime  # RFC 2822 날짜 파싱용

# ==================== 설정 구간 (여기를 수정하세요!) ====================
TELEGRAM_BOT_TOKEN = "8180938946:AAHgoRR7Tt_3J_gyENJXt32qGa0kJ5nQxGM"  # 여기에 텔레그램 봇 토큰을 입력하세요 (예: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
TELEGRAM_CHAT_ID = "143110040"    # 여기에 텔레그램 채팅 ID를 입력하세요 (예: "123456789")
# ========================================================================

# 중복 전송 방지를 위한 파일명
SENT_NEWS_FILE = "sent_news.txt"

# 한국어 검색 키워드 리스트
KOREAN_KEYWORDS = [
    "골프장 인수",
    "골프장 매각",
    "골프장 M&A",
    "골프장 IPO",
    "골프장 사모펀드",
    "PEF 골프"
]

# 영어 검색 키워드 리스트
ENGLISH_KEYWORDS = [
    "Golf course acquisition",
    "Golf course M&A",
    "Golf course IPO",
    "Private Equity Golf",
    "Golf investment deal"
]

# 진성 뉴스를 구분하기 위한 필수 키워드 (이 중 하나라도 포함되어야 함)
FILTER_KEYWORDS = [
    # 한국어
    "인수", "매각", "투자", "딜", "사모펀드", "PEF", "M&A", "IPO", "상장",
    # 영어
    "acquisition", "deal", "capital", "investment", "private equity",
    "merger", "IPO", "buyout", "acquire", "purchase"
]

# 제외할 노이즈 키워드 (이것이 포함되면 제외)
EXCLUDE_KEYWORDS = [
    "대회", "토너먼트", "레슨", "우승", "챔피언십", "타수", "스윙",
    "tournament", "championship", "lesson", "winner", "score", "swing"
]


def load_sent_news():
    """
    이미 전송한 뉴스 목록을 파일에서 불러오는 함수
    반환: 전송한 뉴스 해시값들의 집합(set)
    """
    try:
        with open(SENT_NEWS_FILE, 'r', encoding='utf-8') as f:
            # 파일의 각 줄을 읽어서 set으로 반환
            return set(line.strip() for line in f)
    except FileNotFoundError:
        # 파일이 없으면 빈 set 반환
        return set()


def save_sent_news(news_hash):
    """
    전송한 뉴스의 해시값을 파일에 저장하는 함수
    매개변수: news_hash - 뉴스를 고유하게 식별하는 해시값
    """
    with open(SENT_NEWS_FILE, 'a', encoding='utf-8') as f:
        # 해시값을 파일 끝에 추가
        f.write(news_hash + '\n')


def generate_news_hash(title, link):
    """
    뉴스의 고유 해시값을 생성하는 함수 (중복 체크용)
    매개변수: title - 뉴스 제목, link - 뉴스 링크
    반환: MD5 해시값 (문자열)
    """
    # 제목과 링크를 합쳐서 유니크한 문자열 생성
    unique_string = f"{title}|{link}"
    # MD5 해시로 변환하여 반환
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()


def is_relevant_news(title, summary):
    """
    뉴스가 골프 투자/M&A 관련인지 판단하는 함수
    매개변수: title - 뉴스 제목, summary - 뉴스 요약
    반환: True (관련 뉴스) / False (노이즈)
    """
    # 제목과 요약을 소문자로 변환 (대소문자 구분 없이 검색하기 위해)
    text = (title + ' ' + summary).lower()

    # 먼저 제외 키워드가 있는지 확인
    for exclude in EXCLUDE_KEYWORDS:
        if exclude.lower() in text:
            # 노이즈 키워드가 발견되면 False 반환
            return False

    # 필수 키워드 중 하나라도 포함되어 있는지 확인
    for keyword in FILTER_KEYWORDS:
        if keyword.lower() in text:
            # 관련 키워드가 발견되면 True 반환
            return True

    # 어떤 키워드도 없으면 False 반환
    return False


def send_telegram_message(title, link):
    """
    텔레그램으로 뉴스를 전송하는 함수
    매개변수: title - 뉴스 제목, link - 뉴스 링크
    반환: True (전송 성공) / False (전송 실패)
    """
    # 텔레그램 메시지 형식 작성 (간결한 포맷: 제목 + 링크)
    message = f"""🏌️ {title}

{link}"""

    # 텔레그램 API URL
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    # 전송할 데이터
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'disable_web_page_preview': False  # 링크 미리보기 활성화
    }

    try:
        # HTTP POST 요청으로 메시지 전송
        response = requests.post(url, data=payload, timeout=10)

        # 응답 코드가 200이면 성공
        if response.status_code == 200:
            print(f"✅ 전송 완료: {title}")
            return True
        else:
            print(f"❌ 전송 실패 (코드 {response.status_code}): {title}")
            return False

    except Exception as e:
        # 에러가 발생해도 프로그램은 계속 실행
        print(f"⚠️ 전송 중 에러 발생: {e}")
        return False


def fetch_google_news(keyword):
    """
    구글 뉴스 RSS에서 특정 키워드로 뉴스를 가져오는 함수 (최근 24시간 이내만)
    매개변수: keyword - 검색할 키워드
    반환: 뉴스 항목 리스트
    """
    # 키워드를 URL 인코딩 (한글, 특수문자 등을 URL에 사용 가능하게 변환)
    encoded_keyword = quote(keyword)

    # 구글 뉴스 RSS URL (최근 뉴스 기준)
    rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"

    try:
        print(f"🔍 검색 중: {keyword}")

        # RSS 피드를 HTTP GET 요청으로 가져오기
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생

        # XML 파싱
        root = ET.fromstring(response.content)

        # 현재 시간 (UTC 기준)
        now = datetime.now(timezone.utc)
        # 24시간 전 시간
        one_day_ago = now - timedelta(days=1)

        # 뉴스 항목 리스트 생성
        entries = []

        # RSS 2.0 형식: channel/item 태그에서 뉴스 추출
        for item in root.findall('.//item'):
            # 제목 추출
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else '제목 없음'

            # 링크 추출
            link_elem = item.find('link')
            link = link_elem.text if link_elem is not None else ''

            # 요약(설명) 추출
            desc_elem = item.find('description')
            summary = desc_elem.text if desc_elem is not None else '요약 없음'

            # 발행일 추출
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    # RFC 2822 형식의 날짜를 datetime으로 변환
                    pub_date = parsedate_to_datetime(pub_date_elem.text)

                    # 24시간 이내의 기사만 포함
                    if pub_date < one_day_ago:
                        continue  # 24시간 이전 기사는 건너뛰기
                except Exception:
                    # 날짜 파싱 실패 시 일단 포함
                    pass

            # 딕셔너리 형태로 저장
            entries.append({
                'title': title,
                'link': link,
                'summary': summary
            })

        # 가져온 뉴스 개수 출력
        print(f"   └─ {len(entries)}개 뉴스 발견 (최근 24시간 이내)")

        # 뉴스 항목 반환
        return entries

    except Exception as e:
        # 에러 발생 시 빈 리스트 반환하고 다음으로 넘어감
        print(f"⚠️ '{keyword}' 검색 중 에러 발생: {e}")
        print("   └─ 다음 키워드로 넘어갑니다...")
        return []


def main():
    """
    메인 실행 함수
    """
    print("=" * 60)
    print("🏌️ 골프 딜 뉴스 수집 봇 시작")
    print("=" * 60)

    # 텔레그램 설정 확인
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ 오류: TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 설정해주세요!")
        return

    # 이미 전송한 뉴스 목록 불러오기
    sent_news = load_sent_news()
    print(f"📁 이미 전송된 뉴스: {len(sent_news)}개\n")

    # 모든 키워드 합치기
    all_keywords = KOREAN_KEYWORDS + ENGLISH_KEYWORDS

    # 수집된 모든 뉴스를 저장할 리스트
    all_news = []

    # 각 키워드로 뉴스 수집
    for keyword in all_keywords:
        # 구글 뉴스에서 해당 키워드로 검색
        entries = fetch_google_news(keyword)

        # 각 뉴스 항목 처리
        for entry in entries:
            try:
                # 뉴스 정보 추출
                title = entry.get('title', '제목 없음')
                link = entry.get('link', '')
                summary = entry.get('summary', '요약 없음')

                # 중복 체크를 위한 해시 생성
                news_hash = generate_news_hash(title, link)

                # 이미 전송한 뉴스면 건너뛰기
                if news_hash in sent_news:
                    continue

                # 관련 뉴스인지 필터링
                if not is_relevant_news(title, summary):
                    continue

                # 조건을 통과한 뉴스 저장
                all_news.append({
                    'title': title,
                    'link': link,
                    'summary': summary,
                    'hash': news_hash
                })

            except Exception as e:
                # 개별 뉴스 처리 중 에러 발생 시
                print(f"⚠️ 뉴스 처리 중 에러 발생: {e}")
                print("   └─ 다음 뉴스로 넘어갑니다...")
                continue

        # API 부하 방지를 위한 짧은 대기 (1초)
        time.sleep(1)

    print(f"\n📊 필터링 결과: 총 {len(all_news)}개의 새로운 딜 뉴스 발견\n")

    # 전송 카운터
    success_count = 0

    # 필터링된 뉴스를 텔레그램으로 전송
    if all_news:
        print("📤 텔레그램 전송 시작...\n")

        for news in all_news:
            # 텔레그램으로 전송
            if send_telegram_message(news['title'], news['link']):
                # 전송 성공 시 파일에 저장
                save_sent_news(news['hash'])
                success_count += 1

            # 텔레그램 API 제한 방지 (메시지 간 1초 대기)
            time.sleep(1)
    else:
        print("ℹ️ 전송할 새로운 뉴스가 없습니다.")

    # 최종 결과 출력
    print("\n" + "=" * 60)
    print(f"✨ 작업 완료!")
    print(f"   - 전송 성공: {success_count}개")
    print(f"   - 전송 실패: {len(all_news) - success_count}개")
    print("=" * 60)


# 스크립트 직접 실행 시에만 main() 함수 호출
if __name__ == "__main__":
    main()
