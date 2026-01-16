/**
 * 2025년 귀속 연말정산 세법 상수
 * 출처: 소득세법 시행령 2025년 개정안
 * @version 1.0.0
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
} as const;

// ========== 근로소득공제 ==========
export const EMPLOYMENT_INCOME_DEDUCTION = [
  { max: 5_000_000, rate: 0.70, fixed: 0 },
  { max: 15_000_000, rate: 0.40, fixed: 3_500_000 },
  { max: 45_000_000, rate: 0.15, fixed: 7_500_000 },
  { max: 100_000_000, rate: 0.05, fixed: 12_000_000 },
  { max: Infinity, rate: 0.02, fixed: 14_750_000 },
] as const;

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
} as const;

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
} as const;

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
} as const;

// ========== 연금저축 세액공제 ==========
export const PENSION_CREDIT = {
  RATE_HIGH: 0.165,              // 총급여 5,500만원 이하: 16.5%
  RATE_LOW: 0.132,               // 총급여 5,500만원 초과: 13.2%
  SALARY_THRESHOLD: 55_000_000,
  LIMITS: {
    PENSION_ONLY: 6_000_000,     // 연금저축만: 600만원
    PENSION_IRP: 9_000_000,      // 연금저축+IRP: 900만원
  },
} as const;

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
} as const;

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
} as const;

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
] as const;

// ========== 검증 한도 ==========
export const VALIDATION = {
  MIN_SALARY: 0,
  MAX_SALARY: 1_000_000_000,     // 최대 10억 (현실적 범위)
  MIN_DEPENDENTS: 0,
  MAX_DEPENDENTS: 20,
  MIN_AGE: 0,
  MAX_AGE: 120,
} as const;

// ========== 기준 연도 ==========
export const TAX_YEAR = {
  TARGET_YEAR: 2025,             // 귀속연도
  FILING_YEAR: 2026,             // 신고연도
} as const;
