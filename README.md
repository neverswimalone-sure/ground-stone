# 🏌️ 골프 딜 뉴스 텔레그램 봇

골프장 투자, M&A, IPO 관련 뉴스를 자동으로 수집해서 텔레그램으로 알려주는 파이썬 봇입니다.

## 📋 주요 기능

- ✅ **자동 뉴스 수집**: 구글 뉴스 RSS를 통해 한국어/영어 키워드로 검색
- ✅ **스마트 필터링**: 골프 대회/레슨 등 노이즈 제거, 진짜 딜 뉴스만 선별
- ✅ **텔레그램 알림**: 제목, 링크, 요약을 깔끔하게 정리해서 전송
- ✅ **중복 방지**: 한 번 보낸 뉴스는 다시 전송하지 않음
- ✅ **에러 처리**: 문제가 발생해도 중단 없이 계속 실행

## 🚀 빠른 시작

### 1. 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2. 텔레그램 봇 설정

#### 2-1. 텔레그램 봇 생성
1. 텔레그램에서 [@BotFather](https://t.me/botfather) 검색
2. `/newbot` 명령어 입력
3. 봇 이름과 username 설정
4. **봇 토큰(Token)** 받기 (예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 2-2. 채팅 ID 확인
1. 생성한 봇과 대화 시작 (아무 메시지나 전송)
2. 웹브라우저에서 아래 URL 접속:
   ```
   https://api.telegram.org/bot<봇토큰>/getUpdates
   ```
3. 응답에서 `"chat":{"id":123456789}` 형태로 **채팅 ID** 찾기

#### 2-3. 코드에 설정 입력
`golf_deal_bot.py` 파일을 열어서 상단 설정 구간을 수정:

```python
TELEGRAM_BOT_TOKEN = "여기에_봇_토큰_입력"  # 2-1에서 받은 토큰
TELEGRAM_CHAT_ID = "여기에_채팅_ID_입력"    # 2-2에서 확인한 ID
```

### 3. 실행

```bash
python golf_deal_bot.py
```

## 📊 검색 키워드

### 한국어
- 골프장 인수
- 골프장 매각
- 골프장 M&A
- 골프장 IPO
- 골프장 사모펀드
- PEF 골프

### 영어
- Golf course acquisition
- Golf course M&A
- Golf course IPO
- Private Equity Golf
- Golf investment deal

## 🎯 필터링 로직

### 포함 키워드 (필수)
뉴스에 다음 단어가 하나라도 있어야 전송:
- 한국어: 인수, 매각, 투자, 딜, 사모펀드, PEF, M&A, IPO, 상장
- 영어: acquisition, deal, capital, investment, private equity, merger, IPO, buyout, acquire, purchase

### 제외 키워드 (노이즈)
다음 단어가 포함되면 제외:
- 한국어: 대회, 토너먼트, 레슨, 우승, 챔피언십, 타수, 스윙
- 영어: tournament, championship, lesson, winner, score, swing

## 🔄 자동 실행 (선택사항)

### Windows (작업 스케줄러)
1. 작업 스케줄러 실행
2. "기본 작업 만들기" 선택
3. 트리거: 매일 오전 9시
4. 작업: `python C:\경로\golf_deal_bot.py`

### Linux/Mac (cron)
```bash
# crontab 편집
crontab -e

# 매일 오전 9시 실행
0 9 * * * /usr/bin/python3 /경로/golf_deal_bot.py
```

## 📁 파일 구조

```
ground-stone/
├── golf_deal_bot.py    # 메인 봇 코드
├── requirements.txt     # 필수 라이브러리 목록
├── sent_news.txt        # 전송된 뉴스 기록 (자동 생성)
└── README.md           # 이 문서
```

## 🛠️ 커스터마이징

### 키워드 추가
`golf_deal_bot.py` 파일의 `KOREAN_KEYWORDS` 또는 `ENGLISH_KEYWORDS` 리스트에 원하는 키워드 추가:

```python
KOREAN_KEYWORDS = [
    "골프장 인수",
    "골프 리조트 투자",  # 추가 예시
]
```

### 필터 조정
- 더 많은 뉴스 받기: `FILTER_KEYWORDS`에서 일부 키워드 제거
- 더 적은 뉴스 받기: `EXCLUDE_KEYWORDS`에 제외할 단어 추가

## 🐛 문제 해결

### "전송 실패" 메시지가 나올 때
- 봇 토큰과 채팅 ID가 정확한지 확인
- 봇과 최소 1회 대화를 시작했는지 확인
- 인터넷 연결 확인

### 뉴스가 너무 많이 올 때
- `EXCLUDE_KEYWORDS`에 제외할 단어 추가
- `FILTER_KEYWORDS` 조건 강화

### 뉴스가 안 올 때
- `sent_news.txt` 파일 삭제 후 재실행 (처음부터 다시 수집)
- 키워드가 너무 구체적인지 확인

## 📧 문의

문제가 발생하면 Issue를 등록해주세요!

---

**Made with ❤️ for Golf M&A Professionals**
