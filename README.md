# Ground Stone 🏌️

Golf Course Audit Report Monitor - 골프장 운영업 감사보고서 자동 알림 텔레그램 봇

## 프로젝트 소개

Ground Stone은 한국의 전자공시시스템(DART)을 모니터링하여 골프장 운영업 법인의 감사보고서 제출을 자동으로 감지하고, 텔레그램 채널로 실시간 알림을 보내주는 봇입니다.

**텔레그램 채널**: @GC_golf_audit_bot

## 주요 기능

- 📊 DART Open API를 통한 실시간 감사보고서 모니터링
- 🏌️ 골프장 운영업(KSIC 91221) 법인 필터링
- 📱 텔레그램 채널 자동 알림
- 🗄️ 중복 알림 방지를 위한 데이터베이스 관리
- ⏰ 주기적 자동 체크 (기본 1시간)
- 📝 모니터링 로그 및 통계

## 빠른 시작

### 1. 사전 준비

다음 항목들이 필요합니다:

1. **DART Open API 키**
   - https://opendart.fss.or.kr/ 에서 회원가입 및 API 키 발급

2. **Telegram Bot 토큰**
   - Telegram에서 @BotFather를 통해 봇 생성
   - Bot 토큰 받기

3. **Telegram 채널**
   - 채널 생성 (예: @GC_golf_audit_bot)
   - 봇을 채널 관리자로 추가
   - "Post Messages" 권한 부여

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/neverswimalone-sure/ground-stone.git
cd ground-stone

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (발급받은 키 입력)
nano .env
```

`.env` 파일 예시:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHANNEL_ID=@GC_golf_audit_bot
DART_API_KEY=your_dart_api_key_here
CHECK_INTERVAL_MINUTES=60
```

### 4. 실행

```bash
# 봇 실행
python main.py
```

## 프로젝트 구조

```
ground-stone/
├── src/
│   ├── bot/                    # Telegram 봇 관련
│   │   ├── notifications.py    # 알림 메시지 포매팅 및 전송
│   │   └── __init__.py
│   ├── dart/                   # DART API 관련
│   │   ├── client.py          # DART API 클라이언트
│   │   └── __init__.py
│   ├── database/              # 데이터베이스 관련
│   │   ├── models.py          # SQLAlchemy 모델
│   │   ├── operations.py      # DB 작업
│   │   └── __init__.py
│   └── scheduler/             # 스케줄링 관련
│       ├── tasks.py           # 주기적 모니터링 작업
│       └── __init__.py
├── config/
│   └── settings.py            # 환경 설정
├── data/                      # 데이터베이스 파일
├── logs/                      # 로그 파일
├── tests/                     # 테스트 파일
├── .env.example               # 환경변수 예시
├── .gitignore
├── requirements.txt           # Python 의존성
├── main.py                    # 프로그램 진입점
├── CLAUDE.MD                  # 프로젝트 상세 문서
└── README.md
```

## 기술 스택

- **Python 3.10+**
- **python-telegram-bot**: Telegram Bot API
- **requests**: DART API 통신
- **SQLAlchemy**: 데이터베이스 ORM
- **APScheduler**: 작업 스케줄링

## 사용 방법

### 자동 모니터링

봇을 실행하면 자동으로:
1. 설정된 주기(기본 1시간)마다 DART에서 새로운 감사보고서 확인
2. 골프장 운영업 법인의 보고서 필터링
3. 새로운 보고서 발견 시 텔레그램 채널에 알림 전송
4. 처리된 보고서 데이터베이스에 저장

### 알림 메시지 형식

```
🏌️ 새로운 감사보고서가 제출되었습니다!

📋 회사명: [회사명]
🏢 종목코드: [종목코드]
📊 보고서: 감사보고서
📅 제출일: 2026년 01월 15일
🔗 링크: [DART 바로가기](링크)

💼 업종: 골프장 운영업
```

## 문제 해결

### 연결 테스트 실패

1. **Telegram Bot Token 확인**
   - BotFather에서 받은 토큰이 정확한지 확인
   - .env 파일에 올바르게 입력되었는지 확인

2. **채널 설정 확인**
   - 봇이 채널 관리자로 추가되었는지 확인
   - 채널 ID가 @로 시작하는지 확인 (예: @GC_golf_audit_bot)

3. **DART API 키 확인**
   - API 키가 활성화되었는지 확인
   - https://opendart.fss.or.kr/에서 키 상태 확인

### 알림이 안 올 경우

1. 로그 파일 확인: `logs/ground-stone.log`
2. 수동 체크 실행하여 에러 확인
3. DART API 호출 제한 확인 (일일 10,000회)

## 개발

### 테스트 실행

```bash
pytest tests/
```

### 코드 포매팅

```bash
black src/
```

### 타입 체크

```bash
mypy src/
```

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 참고 자료

- [DART Open API 문서](https://opendart.fss.or.kr/guide/main.do)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot 문서](https://python-telegram-bot.readthedocs.io/)

---

**면책조항**: 이 프로젝트는 정보 제공 목적으로만 사용됩니다. 모든 재무 정보는 공식 출처를 통해 확인하시기 바랍니다.
