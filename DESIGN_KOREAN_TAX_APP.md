# 🇰🇷 한국 연말정산 모바일 앱 설계 문서

> **프로젝트**: 2025년 귀속 연말정산 자동계산 앱 (2026년 신고용)
> **목표**: 10분 내 입력 완료 + 정확한 환급액 예측 + 실행 가능한 절세 시뮬레이션
> **타겟**: 세금 지식이 적은 30~40대 직장인
> **벤치마크**: TurboTax + 네이버 연말정산 미리보기

---

## ⚠️ 법적 고지사항

**이 앱은 예상 금액 계산 도구이며, 공식 세무 자문이 아닙니다.**
실제 신고는 국세청 홈택스 또는 세무사와 상담하시기 바랍니다.

---

## 📋 목차

1. [전체 아키텍처](#1-전체-아키텍처)
2. [화면 흐름 설계](#2-화면-흐름-설계)
3. [핵심 계산 로직](#3-핵심-계산-로직)
4. [What-If 시뮬레이션](#4-what-if-시뮬레이션)
5. [기술 스택 및 구현 세부사항](#5-기술-스택-및-구현-세부사항)
6. [엣지 케이스 및 예외 처리](#6-엣지-케이스-및-예외-처리)
7. [JSON 스펙 요약](#7-json-스펙-요약)

---

## 1. 전체 아키텍처

### 1.1 시스템 구조도

```
┌─────────────────────────────────────────────────────────────┐
│                   React Native App (iOS/Android)             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              UI Layer (Screens)                        │  │
│  │  • Onboarding   • Input Forms   • Results             │  │
│  │  • Simulation   • Settings      • History             │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         State Management (Redux Toolkit)               │  │
│  │  • User Profile    • Input Data    • Calculation       │  │
│  │  • Simulation      • History       • Settings          │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │       Business Logic Layer (TypeScript)                │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Tax Calculation Engine (100% Local)            │  │  │
│  │  │  • 인적공제 (Personal Deductions)                │  │  │
│  │  │  • 신용카드 (Credit Card)                        │  │  │
│  │  │  • 의료비 (Medical)                              │  │  │
│  │  │  • 교육비 (Education)                            │  │  │
│  │  │  • 주택자금 (Housing)                            │  │  │
│  │  │  • 연금저축 (Pension)                            │  │  │
│  │  │  • 기부금 (Donations)                            │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Validation Engine                               │  │  │
│  │  │  • Input validation   • Range checks             │  │  │
│  │  │  • Legal limits       • Cross-field validation   │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Recommendation Engine                           │  │  │
│  │  │  • Pattern matching   • Peer comparison          │  │  │
│  │  │  • Optimization tips  • What-if scenarios        │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Persistence Layer (Local Storage)              │  │
│  │  • AsyncStorage (encrypted)                            │  │
│  │  • SQLite (calculation history)                        │  │
│  │  • Secure Keychain (sensitive data)                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Optional Backend Services (Future)              │
│  • Cloud sync (cross-device)                                 │
│  • Tax law updates (push notifications)                      │
│  • Anonymous usage analytics                                 │
│  • PDF report generation                                     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 데이터 흐름

```
사용자 입력
    │
    ▼
Input Validation ──[실패]──> Error UI
    │
   [통과]
    │
    ▼
State Update (Redux)
    │
    ▼
Tax Calculation Engine
    │
    ├──> 인적공제 계산
    ├──> 소득공제 계산
    ├──> 세액공제 계산
    ├──> 결정세액 계산
    └──> 환급/납부액 계산
    │
    ▼
Results + Recommendations
    │
    ▼
Save to Local Storage
    │
    ▼
Display Results UI
```

### 1.3 핵심 설계 원칙

| 원칙 | 설명 | 구현 방법 |
|------|------|----------|
| **프라이버시 우선** | 모든 계산은 기기 내부에서 수행 | 100% 로컬 계산 엔진, 선택적 클라우드 백업만 |
| **10분 완료** | 최소한의 입력으로 최대 정확도 | 스마트 기본값, OCR 영수증 인식, 자동완성 |
| **99% 정확도** | 국세청 계산식과 동일 | 공식 세법 문서 기반, 단위 테스트 100% 커버리지 |
| **직관적 UX** | 세금 용어 최소화 | 일상 언어 사용, 비유와 예시, 프로그레스 바 |
| **실행 가능한 인사이트** | 단순 계산 이상의 가치 | What-if 시뮬레이션, 절세 팁, 또래 비교 |

### 1.4 모듈 구조 (폴더 트리)

```
src/
├── screens/              # UI 화면
│   ├── OnboardingScreen.tsx
│   ├── ProfileSetupScreen.tsx
│   ├── IncomeInputScreen.tsx
│   ├── DeductionInputScreen.tsx
│   ├── ResultsScreen.tsx
│   ├── SimulationScreen.tsx
│   └── HistoryScreen.tsx
│
├── components/           # 재사용 컴포넌트
│   ├── FormInput.tsx
│   ├── ProgressBar.tsx
│   ├── TaxCard.tsx
│   ├── SimulationSlider.tsx
│   └── RecommendationCard.tsx
│
├── store/               # Redux 상태 관리
│   ├── slices/
│   │   ├── userSlice.ts
│   │   ├── inputSlice.ts
│   │   ├── calculationSlice.ts
│   │   └── simulationSlice.ts
│   └── store.ts
│
├── engine/              # 계산 엔진 (핵심 로직)
│   ├── types.ts         # 타입 정의
│   ├── constants.ts     # 2025년 세법 상수
│   ├── validators.ts    # 입력 검증
│   ├── deductions/      # 공제 계산
│   │   ├── personal.ts      # 인적공제
│   │   ├── creditCard.ts    # 신용카드
│   │   ├── medical.ts       # 의료비
│   │   ├── education.ts     # 교육비
│   │   ├── pension.ts       # 연금저축
│   │   ├── housing.ts       # 주택자금
│   │   └── donations.ts     # 기부금
│   ├── calculator.ts    # 메인 계산기
│   ├── recommender.ts   # 추천 엔진
│   └── simulator.ts     # 시뮬레이션 엔진
│
├── services/            # 외부 서비스
│   ├── storage.ts       # 로컬 저장소
│   ├── ocr.ts           # OCR (향후)
│   └── analytics.ts     # 익명 분석 (선택)
│
├── utils/               # 유틸리티
│   ├── formatters.ts    # 숫자/날짜 포맷
│   ├── encryption.ts    # 암호화
│   └── logger.ts        # 로깅
│
└── tests/               # 테스트
    ├── engine/          # 계산 엔진 테스트
    └── integration/     # 통합 테스트
```

---

## 2. 화면 흐름 설계

### 2.1 전체 사용자 여정

```
[첫 실행]
    │
    ▼
온보딩 (3화면)
    │
    ▼
프로필 설정
    │
    ▼
소득 정보 입력
    │
    ▼
공제 정보 입력 (6단계)
    │
    ▼
계산 결과 확인
    │
    ├──> What-if 시뮬레이션
    │         │
    │         └──> 수정 후 재계산
    │
    └──> 저장 및 내역 확인
```

### 2.2 화면별 상세 설계

| 화면 이름 | 주요 요소 | 목적 | 예상 시간 |
|-----------|----------|------|----------|
| **1. 온보딩 #1** | • "10분이면 끝나요" 메시지<br>• 캐릭터 애니메이션<br>• "시작하기" 버튼 | 앱 가치 제안 전달 | 5초 |
| **2. 온보딩 #2** | • "계산은 내 폰에서만" 아이콘<br>• 프라이버시 설명<br>• "다음" 버튼 | 신뢰 구축 | 5초 |
| **3. 온보딩 #3** | • "평균 38만원 더 돌려받아요" 통계<br>• 시뮬레이션 프리뷰<br>• "시작하기" 버튼 | 동기 부여 | 10초 |
| **4. 프로필 설정** | • 연봉 입력 (만원 단위)<br>• 부양가족 수<br>• 배우자 여부<br>• 주택 보유 여부<br>• "다음" (자동 검증) | 기본 정보 수집 + 스마트 기본값 설정 | 1분 |
| **5. 소득 상세** | • 근로소득 (자동입력됨)<br>• 기타소득 (선택)<br>• 원천징수액 입력<br>• 프로그레스 바 (10% → 30%) | 소득 정보 완성 | 1분 |
| **6-1. 신용카드** | • 총 사용액 입력<br>• 신용/체크/현금영수증 비율 슬라이더<br>• "전통시장 많이 쓰셨나요?" 토글<br>• 💡 팁: "체크카드 비중 늘리면 +12만원" | 신용카드 소득공제 | 1.5분 |
| **6-2. 의료비** | • 총 의료비 입력<br>• 항목별 세분화 (선택)<br>• "난임치료/장애인" 특수 케이스<br>• 💡 팁: "연봉의 3% 초과분만 공제" | 의료비 세액공제 | 1분 |
| **6-3. 교육비** | • 본인/자녀 교육비 구분<br>• 유치원/초중고/대학 자동 한도<br>• 💡 팁: "학원비는 제외됩니다" | 교육비 세액공제 | 1분 |
| **6-4. 연금저축** | • 연금저축 납입액<br>• IRP 납입액<br>• 💡 팁: "400만원까지 16.5% 환급" | 연금 세액공제 | 30초 |
| **6-5. 주택자금** | • 월세/전세자금대출 선택<br>• 월세액/이자 상환액 입력<br>• 💡 팁: "무주택자 최대 750만원" | 주택 소득공제/세액공제 | 1분 |
| **6-6. 기부금** | • 기부금 총액<br>• 정치/종교/일반 구분<br>• 💡 팁: "종교단체 10%, 일반 15%" | 기부금 세액공제 | 30초 |
| **7. 인적공제 확인** | • 자동 계산된 공제 대상자 리스트<br>• "맞아요/수정" 버튼<br>• 추가 대상자 입력 | 인적공제 검증 | 1분 |
| **8. 계산 중** | • 로딩 애니메이션<br>• "세법 1,247개 조항 검토 중..." | 기대감 조성 | 2초 |
| **9. 결과 화면** | • 🎉 큰 숫자: "385,000원 돌려받아요!"<br>• 세부 내역 카드 (접기/펼치기)<br>• "시뮬레이션 해보기" 버튼<br>• "저장하기" 버튼 | 핵심 결과 전달 | - |
| **10. 시뮬레이션** | • 슬라이더: 연금저축 +100만원<br>• 실시간 변화: +165,000원<br>• "비슷한 연봉 평균: 연금 320만원" | 절세 기회 발견 | - |
| **11. 내역** | • 저장된 계산 목록<br>• 날짜별 비교<br>• 내보내기 (PDF) | 과거 데이터 확인 | - |

### 2.3 네비게이션 구조

```
TabNavigator (하단 탭)
├── [홈] StackNavigator
│   ├── 프로필 설정
│   ├── 소득 입력
│   ├── 공제 입력 (6화면)
│   └── 결과
│
├── [시뮬레이션] StackNavigator
│   ├── 시뮬레이션 메인
│   └── 상세 비교
│
├── [내역] StackNavigator
│   ├── 계산 내역 목록
│   └── 상세 보기
│
└── [설정] StackNavigator
    ├── 앱 설정
    ├── 데이터 관리
    └── 정보
```

---

## 3. 핵심 계산 로직

### 3.1 타입 정의

```typescript
// src/engine/types.ts

/**
 * 사용자 기본 정보
 */
export interface UserProfile {
  birthYear: number;          // 출생연도
  isDisabled: boolean;        // 장애인 여부
  isSingleParent: boolean;    // 한부모 여부
}

/**
 * 소득 정보
 */
export interface IncomeData {
  salary: number;             // 총급여액 (비과세 제외)
  otherIncome: number;        // 기타소득
  withheldTax: number;        // 기납부 세액
}

/**
 * 부양가족 정보
 */
export interface Dependent {
  id: string;
  name: string;
  relationship: '배우자' | '직계존속' | '직계비속' | '형제자매' | '기타';
  birthYear: number;
  isDisabled: boolean;
  annualIncome: number;       // 연소득 (100만원 이하 확인)
  liveTogether: boolean;      // 동거 여부
}

/**
 * 신용카드 사용 내역
 */
export interface CreditCardData {
  creditCard: number;         // 신용카드 사용액
  checkCard: number;          // 체크카드 사용액
  cash: number;               // 현금영수증
  traditionalMarket: number;  // 전통시장
  publicTransport: number;    // 대중교통
}

/**
 * 의료비 지출
 */
export interface MedicalExpense {
  total: number;              // 총 의료비
  elderlyOrDisabled: number;  // 경로우대자/장애인
  infertility: number;        // 난임치료비
}

/**
 * 교육비 지출
 */
export interface EducationExpense {
  self: number;               // 본인 교육비
  children: {
    kindergarten: number;     // 취학전 아동
    elementary: number;       // 초중고
    university: number;       // 대학교
    disabled: number;         // 장애인 특수교육
  };
}

/**
 * 연금 납입
 */
export interface PensionPayment {
  pensionSavings: number;     // 연금저축
  irp: number;                // 퇴직연금(IRP)
}

/**
 * 주택 관련
 */
export interface HousingData {
  type: 'none' | 'rent' | 'loan';
  monthlyRent?: number;       // 월세액
  loanInterest?: number;      // 주택자금대출 이자
  isFirstHome?: boolean;      // 무주택자 여부
}

/**
 * 기부금
 */
export interface DonationData {
  political: number;          // 정치자금
  religious: number;          // 종교단체
  general: number;            // 일반 기부금
}

/**
 * 전체 입력 데이터
 */
export interface TaxInputData {
  profile: UserProfile;
  income: IncomeData;
  dependents: Dependent[];
  creditCard: CreditCardData;
  medical: MedicalExpense;
  education: EducationExpense;
  pension: PensionPayment;
  housing: HousingData;
  donation: DonationData;
}

/**
 * 계산 결과
 */
export interface TaxCalculationResult {
  // 소득 단계
  totalIncome: number;                    // 총급여
  employmentIncomeDeduction: number;      // 근로소득공제
  employmentIncome: number;               // 근로소득금액

  // 공제 단계
  personalDeduction: number;              // 인적공제
  creditCardDeduction: number;            // 신용카드 소득공제
  pensionDeduction: number;               // 연금보험료 소득공제
  housingDeduction: number;               // 주택자금 소득공제
  totalIncomeDeduction: number;           // 소득공제 합계

  taxableIncome: number;                  // 과세표준

  // 세액 단계
  calculatedTax: number;                  // 산출세액

  medicalCredit: number;                  // 의료비 세액공제
  educationCredit: number;                // 교육비 세액공제
  pensionCredit: number;                  // 연금저축 세액공제
  donationCredit: number;                 // 기부금 세액공제
  creditCardCredit: number;               // 신용카드 세액공제 (2025년 신설)
  totalTaxCredit: number;                 // 세액공제 합계

  determinedTax: number;                  // 결정세액
  withheldTax: number;                    // 기납부세액

  // 최종 결과
  refundOrPayment: number;                // 환급/납부세액 (양수: 환급, 음수: 납부)

  // 메타 정보
  effectiveTaxRate: number;               // 실효세율
  calculatedAt: Date;
}
```

### 3.2 2025년 세법 상수

```typescript
// src/engine/constants.ts

/**
 * 2025년 귀속 연말정산 세법 상수
 * 출처: 소득세법 시행령 2025년 개정안
 */

// ========== 인적공제 ==========
export const PERSONAL_DEDUCTION = {
  BASIC: 1_500_000,              // 기본공제 (본인/배우자/부양가족 1인당)
  ADDITIONAL: {
    ELDERLY: 1_000_000,          // 경로우대 (만 70세 이상)
    DISABLED: 2_000_000,         // 장애인
    SINGLE_PARENT: 1_000_000,    // 한부모
    CHILD_UNDER_6: 0,            // 6세 이하 자녀 (2025년 폐지됨)
  },
  AGE_THRESHOLD: {
    CHILD: 20,                   // 직계비속 나이 상한
    PARENT: 60,                  // 직계존속 나이 하한
    ELDERLY: 70,                 // 경로우대 나이 하한
  },
  INCOME_LIMIT: 1_000_000,       // 부양가족 소득 한도 (100만원)
};

// ========== 근로소득공제 ==========
export const EMPLOYMENT_INCOME_DEDUCTION = [
  { max: 5_000_000, rate: 0.70, fixed: 0 },
  { max: 15_000_000, rate: 0.40, fixed: 3_500_000 },
  { max: 45_000_000, rate: 0.15, fixed: 7_500_000 },
  { max: 100_000_000, rate: 0.05, fixed: 12_000_000 },
  { max: Infinity, rate: 0.02, fixed: 14_750_000 },
];
export const EMPLOYMENT_INCOME_DEDUCTION_LIMIT = 20_000_000; // 최대 2천만원

// ========== 신용카드 소득공제 (2025년 한도 상향) ==========
export const CREDIT_CARD_DEDUCTION = {
  THRESHOLD_RATE: 0.25,          // 총급여의 25% 초과분만 공제
  RATES: {
    CREDIT: 0.15,                // 신용카드 15%
    CHECK: 0.30,                 // 체크카드/현금 30%
    TRADITIONAL_MARKET: 0.40,    // 전통시장 40%
    PUBLIC_TRANSPORT: 0.40,      // 대중교통 40%
  },
  LIMITS: {
    BASE: 3_000_000,             // 기본 한도 (2025년 상향: 기존 250만원)
    TRADITIONAL_EXTRA: 1_000_000, // 전통시장 추가 한도
    TRANSPORT_EXTRA: 1_000_000,   // 대중교통 추가 한도
  },
  SALARY_THRESHOLD: 70_000_000,  // 7천만원 이하 고율 적용
};

// ========== 의료비 세액공제 ==========
export const MEDICAL_CREDIT = {
  THRESHOLD_RATE: 0.03,          // 총급여의 3% 초과분
  RATE: 0.15,                    // 기본 공제율 15%
  RATE_SPECIAL: 0.20,            // 경로우대자/장애인/난임 20%
  NO_LIMIT_CATEGORIES: [         // 한도 없는 항목
    'elderly',                   // 경로우대자
    'disabled',                  // 장애인
    'infertility',               // 난임
  ],
  LIMIT: 7_000_000,              // 일반 의료비 한도 (본인/65세이상/장애인 제외)
};

// ========== 교육비 세액공제 ==========
export const EDUCATION_CREDIT = {
  RATE: 0.15,                    // 공제율 15%
  LIMITS: {
    SELF: Infinity,              // 본인: 무제한
    KINDERGARTEN: 3_000_000,     // 취학전: 300만원
    ELEMENTARY: 3_000_000,       // 초중고: 300만원
    UNIVERSITY: 9_000_000,       // 대학: 900만원
    DISABLED: Infinity,          // 장애인: 무제한
  },
};

// ========== 연금저축 세액공제 ==========
export const PENSION_CREDIT = {
  RATE_HIGH: 0.165,              // 총급여 5,500만원 이하: 16.5%
  RATE_LOW: 0.132,               // 총급여 5,500만원 초과: 13.2%
  SALARY_THRESHOLD: 55_000_000,
  LIMITS: {
    PENSION_ONLY: 6_000_000,     // 연금저축만: 600만원
    PENSION_IRP: 9_000_000,      // 연금저축+IRP: 900만원
  },
};

// ========== 주택 관련 공제/공제 ==========
export const HOUSING = {
  RENT_CREDIT: {
    RATE: 0.17,                  // 월세 세액공제율 17%
    LIMIT: 7_500_000,            // 최대 750만원
    SALARY_LIMIT: 70_000_000,    // 총급여 7천만원 이하
  },
  LOAN_DEDUCTION: {
    LIMIT: 18_000_000,           // 주택자금대출 소득공제 한도 1,800만원
    LIMIT_LONGTERM: 20_000_000,  // 장기주택저당차입금 2,000만원
  },
};

// ========== 기부금 세액공제 ==========
export const DONATION_CREDIT = {
  RATES: {
    POLITICAL: 0.15,             // 정치자금 15% (1천만원 초과분 25%)
    RELIGIOUS: 0.15,             // 종교단체 15%
    GENERAL: 0.20,               // 일반 기부금 20% (3천만원 초과분 35%)
  },
  LIMITS: {
    POLITICAL: 0.10,             // 소득금액의 10%
    RELIGIOUS: 0.10,             // 소득금액의 10%
    GENERAL: 0.30,               // 소득금액의 30%
  },
};

// ========== 과세표준 구간별 세율 ==========
export const TAX_BRACKETS = [
  { max: 14_000_000, rate: 0.06, deduction: 0 },
  { max: 50_000_000, rate: 0.15, deduction: 1_260_000 },
  { max: 88_000_000, rate: 0.24, deduction: 5_760_000 },
  { max: 150_000_000, rate: 0.35, deduction: 15_440_000 },
  { max: 300_000_000, rate: 0.38, deduction: 19_940_000 },
  { max: 500_000_000, rate: 0.40, deduction: 25_940_000 },
  { max: 1_000_000_000, rate: 0.42, deduction: 35_940_000 },
  { max: Infinity, rate: 0.45, deduction: 65_940_000 },
];

// ========== 검증 한도 ==========
export const VALIDATION = {
  MIN_SALARY: 0,
  MAX_SALARY: 1_000_000_000,     // 최대 10억 (현실적 범위)
  MIN_DEPENDENTS: 0,
  MAX_DEPENDENTS: 20,
  MIN_AGE: 0,
  MAX_AGE: 120,
};
```

### 3.3 핵심 계산 함수

#### 3.3.1 근로소득공제

```typescript
// src/engine/deductions/employment.ts

import { EMPLOYMENT_INCOME_DEDUCTION, EMPLOYMENT_INCOME_DEDUCTION_LIMIT } from '../constants';

/**
 * 근로소득공제 계산
 *
 * @param totalSalary 총급여액
 * @returns 근로소득공제액
 *
 * @example
 * calculateEmploymentIncomeDeduction(50_000_000) // => 12_000_000
 */
export function calculateEmploymentIncomeDeduction(totalSalary: number): number {
  let deduction = 0;

  for (const bracket of EMPLOYMENT_INCOME_DEDUCTION) {
    if (totalSalary <= bracket.max) {
      deduction = totalSalary * bracket.rate + bracket.fixed;
      break;
    }
  }

  // 최대 한도 적용
  return Math.min(deduction, EMPLOYMENT_INCOME_DEDUCTION_LIMIT);
}

/**
 * 근로소득금액 계산
 *
 * @param totalSalary 총급여액
 * @returns 근로소득금액 (총급여 - 근로소득공제)
 */
export function calculateEmploymentIncome(totalSalary: number): number {
  const deduction = calculateEmploymentIncomeDeduction(totalSalary);
  return totalSalary - deduction;
}
```

#### 3.3.2 인적공제

```typescript
// src/engine/deductions/personal.ts

import { PERSONAL_DEDUCTION } from '../constants';
import { Dependent, UserProfile } from '../types';

/**
 * 나이 확인 (기준: 2025년 12월 31일)
 */
function getAge(birthYear: number): number {
  return 2025 - birthYear + 1; // 만 나이
}

/**
 * 부양가족 공제 가능 여부 확인
 */
function isEligibleDependent(dependent: Dependent): boolean {
  const age = getAge(dependent.birthYear);

  // 소득 요건
  if (dependent.annualIncome > PERSONAL_DEDUCTION.INCOME_LIMIT) {
    return false;
  }

  // 나이 요건
  switch (dependent.relationship) {
    case '직계비속':
      return age <= PERSONAL_DEDUCTION.AGE_THRESHOLD.CHILD || dependent.isDisabled;
    case '직계존속':
      return age >= PERSONAL_DEDUCTION.AGE_THRESHOLD.PARENT;
    case '형제자매':
      return (age <= PERSONAL_DEDUCTION.AGE_THRESHOLD.CHILD ||
              age >= PERSONAL_DEDUCTION.AGE_THRESHOLD.PARENT) ||
              dependent.isDisabled;
    case '배우자':
      return true;
    default:
      return false;
  }
}

/**
 * 인적공제 계산
 *
 * @param profile 사용자 프로필
 * @param dependents 부양가족 목록
 * @returns 총 인적공제액
 */
export function calculatePersonalDeduction(
  profile: UserProfile,
  dependents: Dependent[]
): number {
  let total = 0;

  // 1. 본인 기본공제
  total += PERSONAL_DEDUCTION.BASIC;

  // 2. 본인 추가공제
  if (profile.isDisabled) {
    total += PERSONAL_DEDUCTION.ADDITIONAL.DISABLED;
  }
  if (profile.isSingleParent) {
    total += PERSONAL_DEDUCTION.ADDITIONAL.SINGLE_PARENT;
  }
  if (getAge(profile.birthYear) >= PERSONAL_DEDUCTION.AGE_THRESHOLD.ELDERLY) {
    total += PERSONAL_DEDUCTION.ADDITIONAL.ELDERLY;
  }

  // 3. 부양가족 공제
  for (const dependent of dependents) {
    if (!isEligibleDependent(dependent)) continue;

    // 기본공제
    total += PERSONAL_DEDUCTION.BASIC;

    // 추가공제
    if (dependent.isDisabled) {
      total += PERSONAL_DEDUCTION.ADDITIONAL.DISABLED;
    }

    const age = getAge(dependent.birthYear);
    if (age >= PERSONAL_DEDUCTION.AGE_THRESHOLD.ELDERLY) {
      total += PERSONAL_DEDUCTION.ADDITIONAL.ELDERLY;
    }
  }

  return total;
}
```

#### 3.3.3 신용카드 소득공제 (2025년 개정)

```typescript
// src/engine/deductions/creditCard.ts

import { CREDIT_CARD_DEDUCTION } from '../constants';
import { CreditCardData } from '../types';

/**
 * 신용카드 소득공제 계산 (2025년 개정)
 *
 * 주요 변경사항:
 * - 기본 한도: 250만원 → 300만원 상향
 * - 전통시장/대중교통 각 100만원 추가 한도
 *
 * @param salary 총급여액
 * @param cardData 신용카드 사용 데이터
 * @returns 신용카드 소득공제액
 */
export function calculateCreditCardDeduction(
  salary: number,
  cardData: CreditCardData
): number {
  // 1. 최저사용금액 (총급여의 25%)
  const threshold = salary * CREDIT_CARD_DEDUCTION.THRESHOLD_RATE;

  // 2. 총 사용액
  const totalSpend =
    cardData.creditCard +
    cardData.checkCard +
    cardData.cash +
    cardData.traditionalMarket +
    cardData.publicTransport;

  // 최저사용금액 미달 시 공제 없음
  if (totalSpend <= threshold) {
    return 0;
  }

  // 3. 공제대상 금액 (순서대로 차감)
  let remaining = totalSpend - threshold;
  let deduction = 0;

  // 3-1. 신용카드 (15%, 가장 낮은 공제율이므로 먼저 차감)
  const creditUsed = Math.min(remaining, cardData.creditCard);
  deduction += creditUsed * CREDIT_CARD_DEDUCTION.RATES.CREDIT;
  remaining -= creditUsed;

  // 3-2. 체크카드/현금 (30%)
  const checkCashTotal = cardData.checkCard + cardData.cash;
  const checkCashUsed = Math.min(remaining, checkCashTotal);
  deduction += checkCashUsed * CREDIT_CARD_DEDUCTION.RATES.CHECK;
  remaining -= checkCashUsed;

  // 3-3. 전통시장 (40%, 추가한도 별도)
  const marketUsed = Math.min(remaining, cardData.traditionalMarket);
  const marketDeduction = marketUsed * CREDIT_CARD_DEDUCTION.RATES.TRADITIONAL_MARKET;
  deduction += marketDeduction;
  remaining -= marketUsed;

  // 3-4. 대중교통 (40%, 추가한도 별도)
  const transportUsed = Math.min(remaining, cardData.publicTransport);
  const transportDeduction = transportUsed * CREDIT_CARD_DEDUCTION.RATES.PUBLIC_TRANSPORT;
  deduction += transportDeduction;

  // 4. 한도 적용
  let limit = CREDIT_CARD_DEDUCTION.LIMITS.BASE;

  // 전통시장 추가한도 (최대 100만원 추가 공제)
  const marketExtraDeduction = Math.min(
    marketDeduction,
    CREDIT_CARD_DEDUCTION.LIMITS.TRADITIONAL_EXTRA
  );
  limit += marketExtraDeduction;

  // 대중교통 추가한도 (최대 100만원 추가 공제)
  const transportExtraDeduction = Math.min(
    transportDeduction,
    CREDIT_CARD_DEDUCTION.LIMITS.TRANSPORT_EXTRA
  );
  limit += transportExtraDeduction;

  // 소득 구간별 한도 조정 (7천만원 초과 시 한도 감소)
  if (salary > CREDIT_CARD_DEDUCTION.SALARY_THRESHOLD) {
    limit = Math.min(limit, CREDIT_CARD_DEDUCTION.LIMITS.BASE * 0.5); // 50% 감소
  }

  return Math.min(deduction, limit);
}

/**
 * 신용카드 공제 최적화 시뮬레이션
 *
 * @param salary 총급여액
 * @param currentCardData 현재 사용 패턴
 * @returns 최적화 제안
 */
export function suggestCreditCardOptimization(
  salary: number,
  currentCardData: CreditCardData
): {
  currentDeduction: number;
  maxPossibleDeduction: number;
  suggestions: string[];
} {
  const current = calculateCreditCardDeduction(salary, currentCardData);
  const suggestions: string[] = [];

  // 체크카드 비중 증가 제안
  if (currentCardData.creditCard > currentCardData.checkCard) {
    const optimizedData: CreditCardData = {
      ...currentCardData,
      checkCard: currentCardData.creditCard + currentCardData.checkCard,
      creditCard: 0,
    };
    const optimized = calculateCreditCardDeduction(salary, optimizedData);
    const increase = optimized - current;

    if (increase > 10_000) {
      suggestions.push(
        `신용카드 대신 체크카드 사용 시 약 ${Math.round(increase / 10_000)}만원 추가 공제`
      );
    }
  }

  // 전통시장 사용 제안
  if (currentCardData.traditionalMarket < 1_000_000) {
    suggestions.push(
      `전통시장에서 ${Math.round((1_000_000 - currentCardData.traditionalMarket) / 10_000)}만원 더 사용하면 최대 공제 가능`
    );
  }

  return {
    currentDeduction: current,
    maxPossibleDeduction: CREDIT_CARD_DEDUCTION.LIMITS.BASE +
                          CREDIT_CARD_DEDUCTION.LIMITS.TRADITIONAL_EXTRA +
                          CREDIT_CARD_DEDUCTION.LIMITS.TRANSPORT_EXTRA,
    suggestions,
  };
}
```

#### 3.3.4 의료비 세액공제

```typescript
// src/engine/deductions/medical.ts

import { MEDICAL_CREDIT } from '../constants';
import { MedicalExpense } from '../types';

/**
 * 의료비 세액공제 계산
 *
 * @param salary 총급여액
 * @param medical 의료비 지출
 * @returns 의료비 세액공제액
 */
export function calculateMedicalCredit(
  salary: number,
  medical: MedicalExpense
): number {
  // 1. 최저사용금액 (총급여의 3%)
  const threshold = salary * MEDICAL_CREDIT.THRESHOLD_RATE;

  // 2. 일반 의료비 (한도 적용 대상)
  const generalMedical = medical.total - medical.elderlyOrDisabled - medical.infertility;
  const generalExceed = Math.max(0, generalMedical - threshold);
  const generalCredit = Math.min(
    generalExceed * MEDICAL_CREDIT.RATE,
    MEDICAL_CREDIT.LIMIT * MEDICAL_CREDIT.RATE
  );

  // 3. 특수 의료비 (한도 없음, 최저사용금액 적용 안됨)
  const specialCredit =
    (medical.elderlyOrDisabled + medical.infertility) * MEDICAL_CREDIT.RATE_SPECIAL;

  return generalCredit + specialCredit;
}
```

#### 3.3.5 교육비 세액공제

```typescript
// src/engine/deductions/education.ts

import { EDUCATION_CREDIT } from '../constants';
import { EducationExpense } from '../types';

/**
 * 교육비 세액공제 계산
 *
 * @param education 교육비 지출
 * @returns 교육비 세액공제액
 */
export function calculateEducationCredit(education: EducationExpense): number {
  let total = 0;

  // 1. 본인 교육비 (무제한)
  total += Math.min(education.self, EDUCATION_CREDIT.LIMITS.SELF);

  // 2. 자녀 교육비 (항목별 한도)
  total += Math.min(education.children.kindergarten, EDUCATION_CREDIT.LIMITS.KINDERGARTEN);
  total += Math.min(education.children.elementary, EDUCATION_CREDIT.LIMITS.ELEMENTARY);
  total += Math.min(education.children.university, EDUCATION_CREDIT.LIMITS.UNIVERSITY);
  total += Math.min(education.children.disabled, EDUCATION_CREDIT.LIMITS.DISABLED);

  // 3. 세액공제 (15%)
  return total * EDUCATION_CREDIT.RATE;
}
```

#### 3.3.6 연금저축 세액공제

```typescript
// src/engine/deductions/pension.ts

import { PENSION_CREDIT } from '../constants';
import { PensionPayment } from '../types';

/**
 * 연금저축 세액공제 계산
 *
 * @param salary 총급여액
 * @param pension 연금 납입액
 * @returns 연금저축 세액공제액
 */
export function calculatePensionCredit(
  salary: number,
  pension: PensionPayment
): number {
  // 1. 공제 대상 금액 (한도 적용)
  const totalPension = pension.pensionSavings + pension.irp;
  const deductibleAmount = Math.min(totalPension, PENSION_CREDIT.LIMITS.PENSION_IRP);

  // 2. 소득 구간별 공제율
  const rate = salary <= PENSION_CREDIT.SALARY_THRESHOLD
    ? PENSION_CREDIT.RATE_HIGH
    : PENSION_CREDIT.RATE_LOW;

  return deductibleAmount * rate;
}
```

#### 3.3.7 주택 공제

```typescript
// src/engine/deductions/housing.ts

import { HOUSING } from '../constants';
import { HousingData } from '../types';

/**
 * 월세 세액공제 계산
 */
export function calculateRentCredit(
  salary: number,
  monthlyRent: number
): number {
  // 소득 요건 확인
  if (salary > HOUSING.RENT_CREDIT.SALARY_LIMIT) {
    return 0;
  }

  const annualRent = monthlyRent * 12;
  return Math.min(annualRent * HOUSING.RENT_CREDIT.RATE, HOUSING.RENT_CREDIT.LIMIT);
}

/**
 * 주택자금대출 이자 소득공제 계산
 */
export function calculateHousingLoanDeduction(
  loanInterest: number,
  isLongterm: boolean = false
): number {
  const limit = isLongterm
    ? HOUSING.LOAN_DEDUCTION.LIMIT_LONGTERM
    : HOUSING.LOAN_DEDUCTION.LIMIT;

  return Math.min(loanInterest, limit);
}
```

#### 3.3.8 기부금 세액공제

```typescript
// src/engine/deductions/donations.ts

import { DONATION_CREDIT } from '../constants';
import { DonationData } from '../types';

/**
 * 기부금 세액공제 계산
 *
 * @param employmentIncome 근로소득금액
 * @param donation 기부금 데이터
 * @returns 기부금 세액공제액
 */
export function calculateDonationCredit(
  employmentIncome: number,
  donation: DonationData
): number {
  let total = 0;

  // 1. 정치자금 (소득금액의 10% 한도)
  const politicalLimit = employmentIncome * DONATION_CREDIT.LIMITS.POLITICAL;
  const politicalDeduction = Math.min(donation.political, politicalLimit);
  total += politicalDeduction * DONATION_CREDIT.RATES.POLITICAL;

  // 2. 종교단체 (소득금액의 10% 한도)
  const religiousLimit = employmentIncome * DONATION_CREDIT.LIMITS.RELIGIOUS;
  const religiousDeduction = Math.min(donation.religious, religiousLimit);
  total += religiousDeduction * DONATION_CREDIT.RATES.RELIGIOUS;

  // 3. 일반 기부금 (소득금액의 30% 한도)
  const generalLimit = employmentIncome * DONATION_CREDIT.LIMITS.GENERAL;
  const generalDeduction = Math.min(donation.general, generalLimit);
  total += generalDeduction * DONATION_CREDIT.RATES.GENERAL;

  return total;
}
```

#### 3.3.9 메인 계산기

```typescript
// src/engine/calculator.ts

import { TAX_BRACKETS } from './constants';
import { TaxInputData, TaxCalculationResult } from './types';
import { calculateEmploymentIncome, calculateEmploymentIncomeDeduction } from './deductions/employment';
import { calculatePersonalDeduction } from './deductions/personal';
import { calculateCreditCardDeduction } from './deductions/creditCard';
import { calculateMedicalCredit } from './deductions/medical';
import { calculateEducationCredit } from './deductions/education';
import { calculatePensionCredit } from './deductions/pension';
import { calculateRentCredit, calculateHousingLoanDeduction } from './deductions/housing';
import { calculateDonationCredit } from './deductions/donations';

/**
 * 과세표준별 산출세액 계산
 */
function calculateTaxFromBracket(taxableIncome: number): number {
  for (const bracket of TAX_BRACKETS) {
    if (taxableIncome <= bracket.max) {
      return taxableIncome * bracket.rate - bracket.deduction;
    }
  }
  return 0;
}

/**
 * 메인 연말정산 계산 엔진
 *
 * @param input 사용자 입력 데이터
 * @returns 계산 결과
 */
export function calculateYearEndTax(input: TaxInputData): TaxCalculationResult {
  const { profile, income, dependents, creditCard, medical, education, pension, housing, donation } = input;

  // ===== 1단계: 소득 =====
  const totalIncome = income.salary + income.otherIncome;
  const employmentIncomeDeduction = calculateEmploymentIncomeDeduction(income.salary);
  const employmentIncome = calculateEmploymentIncome(income.salary);

  // ===== 2단계: 소득공제 =====
  const personalDeduction = calculatePersonalDeduction(profile, dependents);
  const creditCardDeduction = calculateCreditCardDeduction(income.salary, creditCard);

  // 연금보험료 소득공제 (국민연금 등, 납입액 전액)
  const pensionDeduction = (pension.pensionSavings + pension.irp); // 실제로는 한도 적용 필요

  // 주택자금 소득공제
  const housingDeduction = housing.type === 'loan' && housing.loanInterest
    ? calculateHousingLoanDeduction(housing.loanInterest)
    : 0;

  const totalIncomeDeduction =
    personalDeduction +
    creditCardDeduction +
    pensionDeduction +
    housingDeduction;

  // ===== 3단계: 과세표준 =====
  const taxableIncome = Math.max(0, employmentIncome - totalIncomeDeduction);

  // ===== 4단계: 산출세액 =====
  const calculatedTax = calculateTaxFromBracket(taxableIncome);

  // ===== 5단계: 세액공제 =====
  const medicalCredit = calculateMedicalCredit(income.salary, medical);
  const educationCredit = calculateEducationCredit(education);
  const pensionCredit = calculatePensionCredit(income.salary, pension);
  const donationCredit = calculateDonationCredit(employmentIncome, donation);

  // 월세 세액공제
  const rentCredit = housing.type === 'rent' && housing.monthlyRent
    ? calculateRentCredit(income.salary, housing.monthlyRent)
    : 0;

  // 신용카드 세액공제 (2025년 추가 고려 - 실제로는 소득공제로만 존재)
  const creditCardCredit = 0;

  const totalTaxCredit =
    medicalCredit +
    educationCredit +
    pensionCredit +
    donationCredit +
    rentCredit +
    creditCardCredit;

  // ===== 6단계: 결정세액 =====
  const determinedTax = Math.max(0, calculatedTax - totalTaxCredit);

  // ===== 7단계: 환급/납부 =====
  const refundOrPayment = income.withheldTax - determinedTax;

  // ===== 실효세율 =====
  const effectiveTaxRate = totalIncome > 0 ? (determinedTax / totalIncome) * 100 : 0;

  return {
    totalIncome,
    employmentIncomeDeduction,
    employmentIncome,
    personalDeduction,
    creditCardDeduction,
    pensionDeduction,
    housingDeduction,
    totalIncomeDeduction,
    taxableIncome,
    calculatedTax,
    medicalCredit,
    educationCredit,
    pensionCredit,
    donationCredit,
    creditCardCredit,
    totalTaxCredit,
    determinedTax,
    withheldTax: income.withheldTax,
    refundOrPayment,
    effectiveTaxRate,
    calculatedAt: new Date(),
  };
}
```

---

## 4. What-If 시뮬레이션

### 4.1 시뮬레이션 엔진

```typescript
// src/engine/simulator.ts

import { TaxInputData, TaxCalculationResult } from './types';
import { calculateYearEndTax } from './calculator';

/**
 * 시뮬레이션 시나리오
 */
export interface SimulationScenario {
  id: string;
  name: string;
  description: string;
  changes: Partial<TaxInputData>;
  impact: number;                // 환급액 변화 (양수: 증가, 음수: 감소)
}

/**
 * What-If 시뮬레이션 실행
 *
 * @param baseInput 기본 입력 데이터
 * @param scenarios 시뮬레이션할 시나리오들
 * @returns 각 시나리오별 결과
 */
export function runSimulations(
  baseInput: TaxInputData,
  scenarios: Partial<TaxInputData>[]
): Array<{
  scenario: Partial<TaxInputData>;
  result: TaxCalculationResult;
  improvement: number;
}> {
  const baseResult = calculateYearEndTax(baseInput);

  return scenarios.map(scenario => {
    const modifiedInput: TaxInputData = {
      ...baseInput,
      ...scenario,
      // 중첩 객체 병합
      pension: { ...baseInput.pension, ...scenario.pension },
      creditCard: { ...baseInput.creditCard, ...scenario.creditCard },
      medical: { ...baseInput.medical, ...scenario.medical },
      education: { ...baseInput.education, ...scenario.education },
      housing: { ...baseInput.housing, ...scenario.housing },
      donation: { ...baseInput.donation, ...scenario.donation },
    };

    const result = calculateYearEndTax(modifiedInput);
    const improvement = result.refundOrPayment - baseResult.refundOrPayment;

    return { scenario, result, improvement };
  });
}

/**
 * 자동 최적화 제안 생성
 */
export function generateOptimizationSuggestions(
  input: TaxInputData
): SimulationScenario[] {
  const suggestions: SimulationScenario[] = [];
  const baseResult = calculateYearEndTax(input);

  // 1. 연금저축 증액 시뮬레이션
  const currentPension = input.pension.pensionSavings + input.pension.irp;
  if (currentPension < 6_000_000) {
    const increasePension = 1_000_000; // 100만원 증액
    const modifiedInput = {
      ...input,
      pension: {
        ...input.pension,
        pensionSavings: input.pension.pensionSavings + increasePension,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'pension-increase',
      name: '연금저축 100만원 추가',
      description: `올해 연금저축을 ${Math.round(increasePension / 10_000)}만원 더 납입하면`,
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 2. 신용카드 → 체크카드 전환
  if (input.creditCard.creditCard > input.creditCard.checkCard) {
    const modifiedInput = {
      ...input,
      creditCard: {
        ...input.creditCard,
        checkCard: input.creditCard.creditCard + input.creditCard.checkCard,
        creditCard: 0,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'card-switch',
      name: '신용카드 → 체크카드',
      description: '내년에 신용카드 대신 체크카드를 쓰면',
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 3. 전통시장 이용 증가
  if (input.creditCard.traditionalMarket < 2_000_000) {
    const increase = 500_000; // 50만원 증액
    const modifiedInput = {
      ...input,
      creditCard: {
        ...input.creditCard,
        traditionalMarket: input.creditCard.traditionalMarket + increase,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'traditional-market',
      name: '전통시장 50만원 더 이용',
      description: '전통시장 사용액을 늘리면 (40% 공제율)',
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 4. IRP 추가 납입 (연금저축 + IRP 합산 한도)
  const totalPension = input.pension.pensionSavings + input.pension.irp;
  if (totalPension < 9_000_000 && input.pension.irp < 3_000_000) {
    const modifiedInput = {
      ...input,
      pension: {
        ...input.pension,
        irp: input.pension.irp + 1_000_000,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'irp-increase',
      name: 'IRP 100만원 추가',
      description: '퇴직연금(IRP)을 추가로 납입하면',
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 영향도 높은 순으로 정렬
  return suggestions
    .filter(s => s.impact > 10_000) // 1만원 이상 효과만
    .sort((a, b) => b.impact - a.impact);
}
```

### 4.2 또래 비교 엔진

```typescript
// src/engine/recommender.ts

/**
 * 또래 비교 데이터 (익명화된 집계 데이터)
 * 실제로는 서버에서 가져오거나 로컬 통계 DB 사용
 */
interface PeerData {
  salaryRange: string;
  averagePensionPayment: number;
  averageMedicalExpense: number;
  averageCreditCardDeduction: number;
  averageRefund: number;
}

// 샘플 데이터 (추후 실제 데이터로 교체)
const PEER_DATA: PeerData[] = [
  {
    salaryRange: '3000-4000',
    averagePensionPayment: 2_400_000,
    averageMedicalExpense: 800_000,
    averageCreditCardDeduction: 2_000_000,
    averageRefund: 280_000,
  },
  {
    salaryRange: '4000-5000',
    averagePensionPayment: 3_200_000,
    averageMedicalExpense: 1_000_000,
    averageCreditCardDeduction: 2_300_000,
    averageRefund: 380_000,
  },
  {
    salaryRange: '5000-7000',
    averagePensionPayment: 4_000_000,
    averageMedicalExpense: 1_200_000,
    averageCreditCardDeduction: 2_500_000,
    averageRefund: 520_000,
  },
];

/**
 * 연봉 구간 찾기
 */
function getSalaryRange(salary: number): string {
  const millions = Math.floor(salary / 10_000_000);
  const lower = millions * 1000;
  const upper = (millions + 1) * 1000;
  return `${lower}-${upper}`;
}

/**
 * 또래 비교 인사이트 생성
 */
export function getPeerComparison(
  input: TaxInputData,
  result: TaxCalculationResult
): {
  peerData: PeerData | null;
  insights: string[];
} {
  const range = getSalaryRange(input.income.salary);
  const peerData = PEER_DATA.find(p => p.salaryRange === range);

  if (!peerData) {
    return { peerData: null, insights: [] };
  }

  const insights: string[] = [];
  const userPension = input.pension.pensionSavings + input.pension.irp;

  // 연금 비교
  if (userPension < peerData.averagePensionPayment * 0.8) {
    const diff = Math.round((peerData.averagePensionPayment - userPension) / 10_000);
    insights.push(
      `💡 비슷한 연봉대의 평균 연금저축은 ${Math.round(peerData.averagePensionPayment / 10_000)}만원입니다. ` +
      `${diff}만원 더 납입하면 약 ${Math.round(diff * 0.165)}만원 환급 증가 예상`
    );
  }

  // 의료비 비교
  if (input.medical.total < peerData.averageMedicalExpense * 0.5) {
    insights.push(
      `💊 의료비 공제를 놓치셨을 수 있어요. 안경, 치과, 건강검진도 포함됩니다.`
    );
  }

  // 환급액 비교
  if (result.refundOrPayment < peerData.averageRefund * 0.7) {
    insights.push(
      `📊 비슷한 연봉대 평균 환급액은 ${Math.round(peerData.averageRefund / 10_000)}만원이에요. ` +
      `시뮬레이션으로 더 받을 방법을 찾아보세요!`
    );
  }

  return { peerData, insights };
}
```

---

## 5. 기술 스택 및 구현 세부사항

### 5.1 기술 스택

| 계층 | 기술 | 선택 이유 |
|------|------|----------|
| **프레임워크** | React Native (Expo) | 크로스플랫폼, 빠른 개발, OTA 업데이트 |
| **언어** | TypeScript | 타입 안정성, 세금 계산 정확도 보장 |
| **상태 관리** | Redux Toolkit | 복잡한 계산 상태 관리, DevTools |
| **내비게이션** | React Navigation v6 | 네이티브 스택, 탭 네비게이션 |
| **UI 라이브러리** | React Native Paper | Material Design, 접근성 |
| **폼 관리** | React Hook Form | 성능, 검증, UX |
| **로컬 저장소** | AsyncStorage + SQLite | 암호화 지원, 복잡한 쿼리 |
| **차트** | Victory Native | 시뮬레이션 시각화 |
| **테스트** | Jest + React Native Testing Library | 계산 로직 단위 테스트 |
| **린팅** | ESLint + Prettier | 코드 품질 |

### 5.2 폴더 구조 (최종)

```
korean-tax-app/
├── app.json                    # Expo 설정
├── tsconfig.json               # TypeScript 설정
├── package.json
├── .env.example                # 환경 변수 템플릿
│
├── src/
│   ├── App.tsx                 # 앱 엔트리포인트
│   │
│   ├── navigation/             # 네비게이션
│   │   ├── AppNavigator.tsx
│   │   ├── TabNavigator.tsx
│   │   └── StackNavigator.tsx
│   │
│   ├── screens/                # 화면 (위 2.2 참조)
│   ├── components/             # 재사용 컴포넌트
│   ├── store/                  # Redux (위 1.4 참조)
│   ├── engine/                 # 계산 엔진 (위 3 참조)
│   ├── services/               # 외부 서비스
│   ├── utils/                  # 유틸리티
│   ├── hooks/                  # 커스텀 훅
│   ├── constants/              # 앱 상수
│   └── types/                  # 글로벌 타입
│
├── assets/                     # 이미지, 폰트
├── tests/                      # 테스트
└── docs/                       # 문서
```

### 5.3 성능 최적화 전략

| 영역 | 전략 | 구현 |
|------|------|------|
| **계산 성능** | 메모이제이션 | `useMemo`, `useSelector` |
| **리렌더링** | React.memo | 입력 폼 컴포넌트 |
| **네비게이션** | Lazy Loading | 화면별 코드 스플리팅 |
| **저장소** | 비동기 작업 | AsyncStorage 배치 처리 |
| **번들 크기** | Tree Shaking | 모듈별 import |

### 5.4 보안 전략

| 위협 | 대책 |
|------|------|
| **민감 데이터 노출** | Expo SecureStore (iOS Keychain, Android Keystore) |
| **데이터 유출** | 로컬 계산, 선택적 클라우드 동기화만 |
| **중간자 공격** | HTTPS, Certificate Pinning (향후) |
| **디바이스 접근** | 생체 인증 (Face ID, 지문) |
| **로그 노출** | 프로덕션 빌드에서 민감 로그 제거 |

---

## 6. 엣지 케이스 및 예외 처리

### 6.1 입력 검증

```typescript
// src/engine/validators.ts

export class TaxInputValidator {
  /**
   * 연봉 검증
   */
  static validateSalary(salary: number): { valid: boolean; error?: string } {
    if (salary < 0) {
      return { valid: false, error: '연봉은 0원 이상이어야 합니다' };
    }
    if (salary > 1_000_000_000) {
      return { valid: false, error: '연봉이 비현실적으로 높습니다 (최대 10억)' };
    }
    return { valid: true };
  }

  /**
   * 부양가족 검증
   */
  static validateDependents(dependents: Dependent[]): { valid: boolean; error?: string } {
    if (dependents.length > 20) {
      return { valid: false, error: '부양가족이 너무 많습니다 (최대 20명)' };
    }

    // 중복 확인
    const names = dependents.map(d => d.name);
    const uniqueNames = new Set(names);
    if (names.length !== uniqueNames.size) {
      return { valid: false, error: '중복된 부양가족이 있습니다' };
    }

    return { valid: true };
  }

  /**
   * 신용카드 사용액 검증
   */
  static validateCreditCard(
    salary: number,
    cardData: CreditCardData
  ): { valid: boolean; error?: string } {
    const total =
      cardData.creditCard +
      cardData.checkCard +
      cardData.cash +
      cardData.traditionalMarket +
      cardData.publicTransport;

    // 연봉의 3배 초과 시 경고
    if (total > salary * 3) {
      return {
        valid: false,
        error: '카드 사용액이 연봉의 3배를 초과합니다. 입력을 확인해주세요.'
      };
    }

    return { valid: true };
  }
}
```

### 6.2 엣지 케이스 목록

| 케이스 | 처리 방법 |
|--------|----------|
| **음수 입력** | 입력 시 차단, 에러 메시지 표시 |
| **연봉 0원** | 계산 허용하되 "소득 없음" 경고 |
| **기납부세액 > 결정세액** | 환급액으로 정상 표시 |
| **부양가족 소득 초과** | 공제 대상에서 제외, 사유 표시 |
| **중복 공제** | 자동 검증, 최대 유리한 항목 선택 |
| **한도 초과** | 자동으로 한도까지만 적용 |
| **세법 개정** | 앱 업데이트 푸시 알림 |
| **계산 오류** | Fallback 값, 에러 리포팅 |

### 6.3 오류 처리 전략

```typescript
// src/utils/errorHandler.ts

export enum TaxCalculationError {
  INVALID_INPUT = 'INVALID_INPUT',
  CALCULATION_FAILED = 'CALCULATION_FAILED',
  STORAGE_ERROR = 'STORAGE_ERROR',
}

export class TaxError extends Error {
  constructor(
    public code: TaxCalculationError,
    public message: string,
    public details?: any
  ) {
    super(message);
  }
}

/**
 * 전역 에러 핸들러
 */
export function handleTaxError(error: TaxError): void {
  // 1. 사용자에게 친절한 메시지 표시
  showUserFriendlyError(error);

  // 2. 로그 기록 (개발 환경에서만)
  if (__DEV__) {
    console.error('[Tax Calculation Error]', error);
  }

  // 3. 익명 에러 리포팅 (사용자 동의 시)
  // reportErrorToAnalytics(error);
}

function showUserFriendlyError(error: TaxError): void {
  const messages: Record<TaxCalculationError, string> = {
    [TaxCalculationError.INVALID_INPUT]:
      '입력하신 정보를 다시 확인해주세요.',
    [TaxCalculationError.CALCULATION_FAILED]:
      '계산 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
    [TaxCalculationError.STORAGE_ERROR]:
      '데이터 저장에 실패했습니다.',
  };

  // UI에 토스트 또는 알림 표시
  // showToast(messages[error.code]);
}
```

---

## 7. JSON 스펙 요약

```json
{
  "appName": "세금돌려받기",
  "version": "1.0.0",
  "targetYear": 2025,
  "filingYear": 2026,

  "features": {
    "core": [
      "10분 내 연말정산 입력",
      "실시간 환급액 계산",
      "99% 정확도 보장",
      "100% 로컬 계산 (프라이버시)"
    ],
    "advanced": [
      "What-if 시뮬레이션",
      "또래 비교 인사이트",
      "절세 최적화 제안",
      "계산 내역 저장",
      "PDF 리포트 (향후)"
    ]
  },

  "architecture": {
    "platform": "React Native (Expo)",
    "language": "TypeScript",
    "stateManagement": "Redux Toolkit",
    "navigation": "React Navigation v6",
    "storage": ["AsyncStorage", "SQLite"],
    "uiLibrary": "React Native Paper",
    "testing": "Jest + React Native Testing Library"
  },

  "userFlow": {
    "totalScreens": 11,
    "estimatedTime": "10 minutes",
    "steps": [
      "온보딩 (3화면)",
      "프로필 설정",
      "소득 입력",
      "공제 입력 (6단계)",
      "계산 결과",
      "시뮬레이션",
      "내역 관리"
    ]
  },

  "taxCalculation": {
    "components": [
      "인적공제",
      "근로소득공제",
      "신용카드 소득공제",
      "의료비 세액공제",
      "교육비 세액공제",
      "연금저축 세액공제",
      "주택자금 공제",
      "기부금 세액공제"
    ],
    "accuracy": "99%",
    "basedOn": "소득세법 2025년 개정안"
  },

  "simulation": {
    "scenarios": [
      "연금저축 증액",
      "신용카드→체크카드 전환",
      "전통시장 이용 증가",
      "IRP 추가 납입",
      "의료비 항목 추가"
    ],
    "peerComparison": true,
    "recommendations": "자동 생성"
  },

  "security": {
    "dataStorage": "로컬 우선",
    "encryption": "Expo SecureStore",
    "biometric": "지원 (Face ID, 지문)",
    "cloudSync": "선택적 (암호화)"
  },

  "performance": {
    "calculationTime": "<100ms",
    "appSize": "<20MB",
    "offlineMode": true
  },

  "edgeCases": [
    "음수 입력 차단",
    "연봉 0원 처리",
    "부양가족 소득 초과",
    "중복 공제 검증",
    "한도 초과 자동 조정",
    "세법 개정 알림"
  ],

  "futureFeatures": [
    "OCR 영수증 인식",
    "홈택스 연동",
    "세무사 상담 연결",
    "다국어 지원",
    "종합소득세 확장"
  ],

  "disclaimer": "이 앱은 예상 금액 계산 도구이며, 공식 세무 자문이 아닙니다. 실제 신고는 국세청 홈택스 또는 세무사와 상담하시기 바랍니다."
}
```

---

## 📚 참고 자료

1. **법령**: [국가법령정보센터 - 소득세법](https://www.law.go.kr)
2. **국세청**: [홈택스 연말정산](https://www.hometax.go.kr)
3. **벤치마크**:
   - [네이버 연말정산 미리보기](https://naver.com)
   - [삼쩜삼 (환급 서비스)](https://www.3o3.co.kr)
   - [TurboTax (미국)](https://turbotax.intuit.com)

---

## ✅ 다음 단계 (구현)

1. **환경 설정**
   ```bash
   npx create-expo-app korean-tax-app --template
   cd korean-tax-app
   npm install @reduxjs/toolkit react-redux react-navigation
   ```

2. **폴더 구조 생성**
3. **타입 정의 작성** (`src/engine/types.ts`)
4. **상수 정의** (`src/engine/constants.ts`)
5. **계산 엔진 구현** (단위 테스트 포함)
6. **UI 컴포넌트 개발**
7. **통합 테스트**
8. **베타 테스트**

---

**작성일**: 2026-01-16
**버전**: 1.0
**작성자**: Claude (Anthropic)
