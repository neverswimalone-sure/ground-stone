# DART 골프장 감사보고서 모니터링 봇

## 프로젝트 개요

이 프로젝트는 전자공시 OPENDART 시스템에 감사보고서를 제출하는 **골프장 운영업** 법인들의 2025년 감사보고서 공시를 모니터링하여 텔레그램으로 알림을 보내는 봇입니다.

## 주요 데이터

- **엑셀 파일**: `기업개황_20260110.xlsx`
- **파일 위치**: 프로젝트 루트 디렉토리(`D:\Project AI\코드늦둥이`)
- **내용**: 전자공시 사이트에 감사보고서를 제출하는 법인 중 **업종명이 골프장 운영업인 회사 약 470개**의 기본 정보
  - 회사명
  - 고유번호
  - 사업자등록번호
  - 주소
  - 설립일 등

이 엑셀 파일에 포함된 회사만 모니터링 대상으로 삼습니다.

## 목표 기능

### 1. 엑셀에서 대상 회사 목록 추출

- `pandas`로 `기업개황_20260110.xlsx`를 읽습니다
- 업종명이 "골프장 운영업"인 행만 필터링합니다
- 각 회사에 대해 DART API 조회에 필요한 최소 식별자(예: 고유번호, 사업자등록번호, 회사명)를 리스트 또는 DataFrame으로 정리합니다

### 2. Open DART API를 이용한 감사보고서 조회

- 환경 변수 `DART_API_KEY`에 Open DART API 키가 설정되어 있다고 가정합니다
- 각 회사별로 DART API를 호출하여 공시 목록을 조회합니다
- 2025년에 제출된 공시 중 "감사보고서"에 해당하는 문서만 필터링하는 로직을 구현합니다
  - 보고서명에 "감사보고서" 포함 여부 등으로 1차 필터링
  - 필요 시 문서 코드/유형 코드로 추가 필터링

**DART API 엔드포인트**:
- 공시검색: `https://opendart.fss.or.kr/api/list.json`
- 필요한 파라미터: `crtfc_key`, `corp_code`, `bgn_de`, `end_de`, `pblntf_ty` 등

### 3. 신규 공시 감지 및 상태 저장

- 이미 알림을 보낸 공시는 다시 보내지 않도록 "상태 저장" 기능을 구현합니다
- 구현 방식:
  - `state.json` 파일에 `{"sent_rcpnos": ["2025-00000001", ...]}` 형태로 접수번호 목록을 저장
  - 또는 SQLite DB에 테이블을 만들어 관리

**실행 시 흐름**:
1. DART에서 2025년 감사보고서 목록 조회
2. 아직 `sent_rcpnos`에 없는 접수번호만 신규로 판단
3. 신규 건에 대해서만 텔레그램 알림 발송 후 `sent_rcpnos`에 추가 저장

### 4. 텔레그램 알림 발송

**환경 변수**:
- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 메시지를 받을 채팅 ID

**텔레그램 Bot API**: `https://api.telegram.org/bot<TOKEN>/sendMessage`

**메시지 포맷 예시**:
```
🏌️ [DART 감사보고서 알림]

회사명: XXX 골프장
고유번호: XXXXXXXX
보고서명: 2025년 사업연도 감사보고서
접수번호: 2025-XXXXX-XXXXX
공시일자: 2025-03-15

🔗 https://dart.fss.or.kr/dsaf001/main.do?rcpNo=2025XXXXXXXXX
```

### 5. 주기 실행을 위한 메인 함수

`run_once()` 함수를 만들어 한 번 실행 시 다음을 수행:
1. 엑셀 로딩 및 대상 회사 목록 생성
2. 회사별 DART 공시 조회
3. 2025년 감사보고서 필터링
4. 신규 건 텔레그램 발송
5. 상태 저장

이 함수가 cron, systemd timer, 서버리스 등에서 주기적으로 호출될 수 있도록 설계합니다.

## 기술 스택

### 언어
- Python 3.8+

### 주요 라이브러리
- `pandas`: 엑셀 파일 처리
- `openpyxl`: 엑셀 파일 읽기 엔진
- `requests` 또는 `httpx`: DART/텔레그램 API 호출
- `python-dotenv`: 환경 변수 로딩

### 실행 환경
- 로컬 또는 서버 환경에서 프로젝트 루트를 워킹 디렉토리로 설정
- 필요한 파일들: `gieobgaehwang_20260110.xlsx`, 소스 코드, state 파일 등

## 프로젝트 구조

```
ground-stone/
├── gieobgaehwang_20260110.xlsx    # 골프장 회사 목록
├── .env                            # 환경 변수 (git ignore)
├── requirements.txt                # Python 의존성
├── state.json                      # 알림 발송 상태 (자동 생성)
├── src/
│   ├── __init__.py
│   ├── company_loader.py          # 엑셀 로딩 및 필터링
│   ├── dart_client.py             # DART API 클라이언트
│   ├── telegram_notifier.py       # 텔레그램 알림
│   ├── state_manager.py           # 상태 저장 관리
│   └── main.py                    # 메인 실행 로직
├── README.md
└── CLAUDE.MD                       # 이 파일
```

## 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력:

```env
DART_API_KEY=your_dart_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

## 설치 및 실행

### 설치
```bash
pip install -r requirements.txt
```

### 실행
```bash
python src/main.py
```

### 주기 실행 (Cron 예시)
```cron
# 매일 오전 9시에 실행
0 9 * * * cd /path/to/ground-stone && python src/main.py
```

## 구현 체크리스트

- [ ] `requirements.txt` 작성
- [ ] `company_loader.py`: 엑셀 로딩 및 골프장 운영업 필터링
- [ ] `dart_client.py`: DART API 래퍼 및 감사보고서 필터링
- [ ] `state_manager.py`: JSON 기반 상태 저장/로드
- [ ] `telegram_notifier.py`: 텔레그램 메시지 발송
- [ ] `main.py`: 전체 로직 통합
- [ ] `.env.example` 작성
- [ ] 테스트 실행 및 디버깅

## DART API 참고사항

### 공시검색 API
- **엔드포인트**: `https://opendart.fss.or.kr/api/list.json`
- **주요 파라미터**:
  - `crtfc_key`: API 인증키
  - `corp_code`: 기업 고유번호 (8자리)
  - `bgn_de`: 시작일자 (YYYYMMDD)
  - `end_de`: 종료일자 (YYYYMMDD)
  - `pblntf_ty`: 공시유형 (A: 정기공시)
  - `page_no`: 페이지 번호
  - `page_count`: 페이지당 건수 (최대 100)

### 감사보고서 식별
- 보고서명에 "감사보고서" 포함
- 보고서 코드: `11011` (사업보고서), `11012` (반기보고서), `11013` (분기보고서), `11014` (등)
- 주로 매년 3-4월에 제출됨

## 주의사항

1. **API Rate Limit**: DART API는 분당 요청 제한이 있을 수 있으므로, 회사별 조회 시 적절한 딜레이(예: 0.5초) 추가
2. **에러 핸들링**: API 호출 실패, 네트워크 오류 등에 대한 예외 처리 필수
3. **로깅**: 실행 기록을 로그 파일로 남겨 디버깅 용이하게 구성
4. **테스트**: 소수의 회사로 먼저 테스트 후 전체 실행

## Claude Code 작업 가이드

Claude Code는 다음을 우선적으로 수행합니다:

1. `gieobgaehwang_20260110.xlsx` 구조를 파악하고, 업종명이 "골프장 운영업"인 행만 필터링하는 Python 코드를 작성
2. 필터링된 회사 리스트에서 DART API 호출에 사용할 식별자 컬럼(예: 고유번호, 사업자등록번호)을 결정하고, 이를 처리하는 헬퍼 함수 작성
3. Open DART API를 감싸는 래퍼 모듈 작성
   - 회사별 2025년 공시 목록 조회
   - 감사보고서만 필터링하는 로직
4. `state.json` 또는 SQLite 기반의 상태 관리 모듈 작성
5. 텔레그램 알림 발송 모듈 작성
6. 위 구성 요소를 사용하는 `run_once()` 또는 `main()` 함수 작성
7. `requirements.txt` 및 간단한 디렉토리 구조 예시 제안

**응답 시 원칙**:
- 최대한 실행 가능한 코드 위주로 답변
- 필요한 경우, 실제로 붙여넣어 사용할 수 있는 형태의 파일별 코드 스켈레톤 제시
- 한글 주석 및 독스트링 사용
- 타입 힌트 활용으로 코드 가독성 향상

## 라이선스

이 프로젝트는 개인 모니터링 목적으로 사용됩니다.

## 문의

프로젝트 관련 문의사항은 이슈를 통해 남겨주세요.
