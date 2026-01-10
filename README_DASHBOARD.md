# ⛳ Golf Course M&A Valuation Dashboard

## 개요
이 대시보드는 골프장 M&A 딜의 EBITDA 및 기업가치(EV)를 실시간으로 분석하는 인터랙티브 투자은행 자문 도구입니다.

## 주요 기능

### 📊 인터랙티브 컨트롤
- **객단가 슬라이더**: 90,000원 ~ 130,000원 (5,000원 단위)
- **내장객 수 슬라이더**: 120,000명 ~ 160,000명 (5,000명 단위)
- **EV/EBITDA 배수 슬라이더**: 5.0x ~ 12.0x (0.5x 단위)

### 📈 실시간 계산
- 매출 (Revenue)
- Operating Expenses
- EBITDA 및 EBITDA Margin
- Enterprise Value (EV)

### 📊 3가지 탭 구성
1. **Sensitivity Analysis**: EBITDA 및 EV 히트맵
2. **Scenario Analysis**: Base/Bull/Bear 시나리오 비교
3. **Deal Summary**: 상세 M&A 보고서 및 CSV 다운로드

## 실행 방법

### 1. Streamlit 대시보드 실행
```bash
streamlit run golf_mna_dashboard.py
```

### 2. 브라우저 접속
대시보드가 자동으로 브라우저에서 열립니다. 일반적으로:
- **로컬 URL**: http://localhost:8501
- **네트워크 URL**: http://YOUR_IP:8501

### 3. 정적 히트맵 생성 (선택사항)
```bash
python golf_ebitda_analysis.py
```
이 명령어는 `golf_ebitda_sensitivity_analysis.png` 파일을 생성합니다.

## 파일 구조
```
.
├── golf_mna_dashboard.py              # Streamlit 인터랙티브 대시보드
├── golf_ebitda_analysis.py            # 정적 히트맵 생성 스크립트
├── golf_ebitda_sensitivity_analysis.png  # 생성된 히트맵 이미지
└── README_DASHBOARD.md                # 이 문서
```

## 기술 스택
- **Streamlit**: 인터랙티브 웹 대시보드
- **Plotly**: 동적 차트 및 히트맵
- **Pandas & NumPy**: 데이터 분석
- **Seaborn & Matplotlib**: 정적 시각화

## 기본 가정
- **홀 수**: 18홀
- **Operating Expense Ratio**: 45% of Revenue
- **Base Case**:
  - 연간 내장객 수: 140,000명
  - 1인당 객단가: 110,000원
  - EBITDA: 84.7억원

## 사용 예시

### 시나리오 1: Bull Case
- 객단가: 130,000원
- 내장객 수: 160,000명
- EV/EBITDA: 10.0x
→ **EV: 1,144억원**

### 시나리오 2: Bear Case
- 객단가: 90,000원
- 내장객 수: 120,000명
- EV/EBITDA: 6.0x
→ **EV: 356억원**

## 주의사항
⚠️ 이 대시보드는 예시 목적으로만 사용됩니다. 실제 M&A 가치평가는 포괄적인 실사(Due Diligence)가 필요합니다.

## 문의
Investment Banking Advisory Team
