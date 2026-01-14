# Ground Stone 설치 및 설정 가이드

이 가이드는 Ground Stone 봇을 처음 설정하는 분들을 위한 단계별 안내서입니다.

## 📋 목차

1. [사전 준비](#사전-준비)
2. [Telegram Bot 생성](#telegram-bot-생성)
3. [DART API 키 발급](#dart-api-키-발급)
4. [프로젝트 설치](#프로젝트-설치)
5. [환경 설정](#환경-설정)
6. [실행 및 테스트](#실행-및-테스트)
7. [문제 해결](#문제-해결)

---

## 사전 준비

### 필요한 것들

- Python 3.10 이상
- Git
- 인터넷 연결
- Telegram 계정
- DART 계정 (무료 회원가입)

---

## Telegram Bot 생성

### 1️⃣ BotFather를 통해 봇 생성

1. **Telegram 앱 실행**

2. **BotFather 검색**
   - 검색창에 `@BotFather` 입력
   - 공식 BotFather (파란 체크마크) 선택

3. **새 봇 생성**
   ```
   /start
   /newbot
   ```

4. **봇 이름 입력**
   - 예: `Golf Audit Monitor`
   - 사용자에게 표시될 이름

5. **봇 username 입력**
   - 예: `golf_audit_monitor_bot`
   - 반드시 `bot`으로 끝나야 함
   - 전역적으로 고유해야 함

6. **토큰 받기**
   - BotFather가 다음과 같은 토큰을 제공합니다:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   - ⚠️ **중요**: 이 토큰은 절대 공개하지 마세요!
   - 이 토큰을 안전한 곳에 복사해두세요

### 2️⃣ Telegram 채널 생성

1. **새 채널 만들기**
   - Telegram 메뉴 → New Channel

2. **채널 정보 입력**
   - Channel name: `Golf Course Audit Reports`
   - Description: 골프장 운영업 감사보고서 알림

3. **채널 타입 선택**
   - Public 채널 선택
   - Username 설정: `GC_golf_audit_bot` (또는 원하는 이름)

4. **채널 생성 완료**
   - Skip을 눌러 구독자 추가 단계 건너뛰기

### 3️⃣ 봇을 채널 관리자로 추가

1. **채널 설정 열기**
   - 채널 이름 클릭 → 설정 아이콘

2. **관리자 추가**
   - "Administrators" 선택
   - "Add Administrator" 클릭

3. **봇 검색 및 추가**
   - 앞서 만든 봇 username 검색
   - 봇 선택

4. **권한 설정**
   - ✅ "Post Messages" 체크
   - 다른 권한은 선택사항
   - "Done" 클릭

---

## DART API 키 발급

### 1️⃣ DART 회원가입

1. **DART 웹사이트 방문**
   - https://opendart.fss.or.kr/

2. **회원가입**
   - 우측 상단 "회원가입" 클릭
   - 정보 입력 및 이메일 인증

3. **로그인**
   - 가입한 계정으로 로그인

### 2️⃣ API 키 발급

1. **API 신청 페이지 이동**
   - 상단 메뉴 "오픈API" 클릭
   - "인증키 신청/관리" 선택

2. **API 키 신청**
   - "신청" 버튼 클릭
   - 사용 목적 입력 (예: "개인 프로젝트 - 감사보고서 모니터링")

3. **API 키 승인 대기**
   - 보통 즉시 승인됨
   - 이메일로 승인 알림 받음

4. **API 키 확인 및 복사**
   - "인증키 신청/관리" 페이지에서 발급된 키 확인
   - 키를 복사하여 안전한 곳에 보관

---

## 프로젝트 설치

### 1️⃣ 저장소 클론

```bash
# HTTPS로 클론
git clone https://github.com/neverswimalone-sure/ground-stone.git
cd ground-stone
```

### 2️⃣ 가상환경 생성 (권장)

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ 의존성 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 환경 설정

### 1️⃣ 환경 변수 파일 생성

```bash
cp .env.example .env
```

### 2️⃣ .env 파일 편집

텍스트 에디터로 `.env` 파일을 열어 다음 정보를 입력합니다:

```bash
# 리눅스/맥
nano .env

# 또는
vim .env

# Windows
notepad .env
```

### 3️⃣ 필수 설정 입력

```env
# Telegram Bot 토큰 (BotFather에서 받은 것)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Telegram 채널 ID (@로 시작, 채널 username)
TELEGRAM_CHANNEL_ID=@GC_golf_audit_bot

# DART API 키 (DART에서 발급받은 것)
DART_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 데이터베이스 경로 (기본값 사용 권장)
DATABASE_URL=sqlite:///data/ground-stone.db

# 체크 주기 (분 단위, 기본 60분)
CHECK_INTERVAL_MINUTES=60

# 로그 레벨 (INFO, DEBUG, WARNING, ERROR)
LOG_LEVEL=INFO
```

### 4️⃣ 설정 확인

모든 필수 항목이 올바르게 입력되었는지 확인:

- ✅ `TELEGRAM_BOT_TOKEN`: 숫자:문자 형식
- ✅ `TELEGRAM_CHANNEL_ID`: @로 시작
- ✅ `DART_API_KEY`: 40자 문자열

---

## 실행 및 테스트

### 1️⃣ 첫 실행

```bash
python main.py
```

### 2️⃣ 로그 확인

다음과 같은 메시지가 출력되어야 합니다:

```
==================================================
Ground Stone - Golf Course Audit Report Monitor
==================================================
Validating configuration...
Initializing database...
Testing connections...
Connected to bot: golf_audit_monitor_bot
✅ Ground Stone 봇이 정상적으로 연결되었습니다.
All connection tests passed
Starting monitor service...
Running manual check...
Found X audit reports
Check completed: X new reports notified
Bot is now running. Press Ctrl+C to stop.
```

### 3️⃣ Telegram 채널 확인

채널에 다음 메시지가 표시되어야 합니다:
```
✅ Ground Stone 봇이 정상적으로 연결되었습니다.
```

### 4️⃣ 백그라운드 실행 (선택사항)

**Linux/Mac (nohup 사용):**
```bash
nohup python main.py > output.log 2>&1 &
```

**Linux/Mac (screen 사용):**
```bash
screen -S ground-stone
python main.py
# Ctrl+A, D를 눌러 detach
```

**systemd 서비스 (Linux):**
`/etc/systemd/system/ground-stone.service` 파일 생성:
```ini
[Unit]
Description=Ground Stone Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/ground-stone
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

서비스 시작:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ground-stone
sudo systemctl start ground-stone
sudo systemctl status ground-stone
```

---

## 문제 해결

### ❌ "TELEGRAM_BOT_TOKEN is required" 에러

**원인**: .env 파일이 없거나 토큰이 입력되지 않음

**해결**:
1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. `TELEGRAM_BOT_TOKEN=` 다음에 실제 토큰이 입력되었는지 확인
3. 따옴표 없이 토큰만 입력했는지 확인

### ❌ "Connection test failed" 에러

**원인**: Telegram 봇 연결 실패

**해결**:
1. 인터넷 연결 확인
2. 봇 토큰이 정확한지 확인
3. 봇이 차단되지 않았는지 확인
4. 채널에 봇이 관리자로 추가되었는지 확인

### ❌ "Chat not found" 에러

**원인**: 채널 ID가 잘못되었거나 봇이 채널에 없음

**해결**:
1. `TELEGRAM_CHANNEL_ID`가 @로 시작하는지 확인
2. 채널 username이 정확한지 확인
3. 봇이 채널 관리자로 추가되었는지 다시 확인
4. "Post Messages" 권한이 부여되었는지 확인

### ❌ DART API 에러

**원인**: DART API 키가 잘못되었거나 만료됨

**해결**:
1. DART 웹사이트에서 API 키 상태 확인
2. API 키를 다시 복사하여 .env에 입력
3. API 일일 호출 한도 확인 (10,000회)

### ❌ "ModuleNotFoundError" 에러

**원인**: 필요한 패키지가 설치되지 않음

**해결**:
```bash
pip install -r requirements.txt
```

### 📝 로그 확인

문제가 계속되면 로그 파일을 확인하세요:
```bash
cat logs/ground-stone.log
```

---

## 다음 단계

✅ 봇이 정상 작동하면:

1. **모니터링 주기 조정**
   - `.env` 파일에서 `CHECK_INTERVAL_MINUTES` 수정

2. **로그 레벨 조정**
   - 상세한 디버깅: `LOG_LEVEL=DEBUG`
   - 운영 환경: `LOG_LEVEL=INFO`

3. **데이터베이스 확인**
   - SQLite 브라우저로 `data/ground-stone.db` 열기
   - 처리된 보고서 내역 확인

4. **채널 공개**
   - 채널을 친구들과 공유
   - 구독자 모집

---

## 지원

문제가 해결되지 않으면:
- GitHub Issues: https://github.com/neverswimalone-sure/ground-stone/issues
- CLAUDE.MD 문서 참고
- README.md 참고

---

**축하합니다! 🎉**
Ground Stone 봇이 이제 골프장 감사보고서를 모니터링하고 있습니다!
