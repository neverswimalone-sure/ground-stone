# DART 골프장 감사보고서 모니터링 봇

전자공시 OPENDART 시스템에서 골프장 운영업 법인들의 감사보고서 공시를 모니터링하여 텔레그램으로 알림을 보내는 자동화 봇입니다.

## 주요 기능

- 📊 골프장 운영업 약 470개 회사의 DART 공시 자동 모니터링
- 🔍 2025년 감사보고서 신규 공시 실시간 감지
- 📱 텔레그램으로 즉시 알림 발송
- 💾 중복 알림 방지를 위한 상태 관리
- 📝 상세한 로깅 및 실행 기록

## 프로젝트 구조

```
ground-stone/
├── 기업개황_20260110.xlsx    # 골프장 회사 목록
├── .env                            # 환경 변수 (git ignore)
├── .env.example                    # 환경 변수 템플릿
├── requirements.txt                # Python 의존성
├── state.json                      # 알림 발송 상태 (자동 생성)
├── dart_monitoring.log             # 실행 로그 (자동 생성)
├── src/
│   ├── __init__.py
│   ├── config.py                  # 설정 관리
│   ├── excel_loader.py            # 엑셀 로딩 및 필터링
│   ├── dart_client.py             # DART API 클라이언트
│   ├── telegram_client.py         # 텔레그램 알림
│   ├── state_store.py             # 상태 저장 관리
│   └── runner.py                  # 메인 실행 로직
├── README.md
└── CLAUDE.MD                       # 프로젝트 상세 문서
```

## 설치 및 설정

### 1. 저장소 클론

```bash
git clone <repository-url>
cd ground-stone
```

### 2. Python 가상환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일을 편집하여 실제 값 입력
# DART_API_KEY: https://opendart.fss.or.kr/ 에서 발급
# TELEGRAM_BOT_TOKEN: BotFather에서 발급
# TELEGRAM_CHAT_ID: 텔레그램 채팅 ID
```

`.env` 파일 예시:
```env
DART_API_KEY=your_actual_dart_api_key
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

### 5. 엑셀 파일 준비

프로젝트 루트에 `기업개황_20260110.xlsx` 파일을 배치하세요.

## 사용 방법

### 설정 테스트

처음 설정 후 모든 것이 정상 작동하는지 확인:

```bash
python src/runner.py --test
```

이 명령은 다음을 확인합니다:
- 환경 변수 설정
- 엑셀 파일 읽기
- 텔레그램 연결
- 상태 저장소 동작

### 모니터링 실행

```bash
python src/runner.py
```

이 명령은:
1. 엑셀에서 골프장 운영업 회사 목록 로드
2. DART API로 각 회사의 2025년 감사보고서 조회
3. 신규 공시만 필터링 (이미 알림 보낸 것 제외)
4. 텔레그램으로 알림 발송
5. 상태 저장 (중복 방지)

### 상태 초기화

모든 알림 기록을 삭제하고 처음부터 다시 시작하려면:

```bash
python src/runner.py --reset-state
```

⚠️ **주의**: 이 명령은 모든 알림 기록을 삭제합니다!

## 주기적 실행 설정

### Linux/Mac - Cron

매일 오전 9시에 자동 실행:

```bash
# crontab 편집
crontab -e

# 다음 라인 추가
0 9 * * * cd /path/to/ground-stone && /path/to/venv/bin/python src/runner.py >> /path/to/cron.log 2>&1
```

### Windows - Task Scheduler

1. 작업 스케줄러 열기
2. "기본 작업 만들기" 클릭
3. 트리거: 매일 오전 9시
4. 작업: `python.exe` 실행
5. 인수: `src/runner.py`
6. 시작 위치: `C:\path\to\ground-stone`

## 개별 모듈 테스트

각 모듈은 독립적으로 테스트할 수 있습니다:

```bash
# 엑셀 로더 테스트
python src/excel_loader.py

# DART 클라이언트 테스트
python src/dart_client.py

# 텔레그램 클라이언트 테스트
python src/telegram_client.py

# 상태 저장소 테스트
python src/state_store.py
```

## 로그 확인

실행 로그는 `dart_monitoring.log` 파일에 저장됩니다:

```bash
# 최근 로그 확인
tail -f dart_monitoring.log

# 전체 로그 확인
cat dart_monitoring.log
```

## 문제 해결

### 엑셀 파일을 찾을 수 없습니다

- `기업개황_20260110.xlsx` 파일이 프로젝트 루트에 있는지 확인
- 파일명이 정확히 일치하는지 확인

### DART API 호출 실패

- `DART_API_KEY`가 올바르게 설정되었는지 확인
- DART API 키가 유효한지 확인 (https://opendart.fss.or.kr/)
- 네트워크 연결 확인

### 텔레그램 메시지가 전송되지 않음

- `TELEGRAM_BOT_TOKEN`이 올바른지 확인
- `TELEGRAM_CHAT_ID`가 올바른지 확인
- 봇이 해당 채팅방에 추가되어 있는지 확인

### 엑셀 컬럼명 오류

- 엑셀 파일의 컬럼명이 예상과 다를 수 있습니다
- `src/excel_loader.py`의 `_find_column` 메서드에서 후보 컬럼명을 확인/수정하세요

## 기술 스택

- **Python 3.8+**
- **pandas**: 엑셀 파일 처리
- **openpyxl**: 엑셀 파일 읽기 엔진
- **requests**: HTTP API 호출
- **python-dotenv**: 환경 변수 관리

## 라이선스

이 프로젝트는 개인 모니터링 목적으로 사용됩니다.

## 참고 문서

- [CLAUDE.MD](./CLAUDE.MD) - 프로젝트 상세 문서 및 Claude Code 작업 가이드
- [DART API 문서](https://opendart.fss.or.kr/guide/main.do)
- [텔레그램 봇 API 문서](https://core.telegram.org/bots/api)
