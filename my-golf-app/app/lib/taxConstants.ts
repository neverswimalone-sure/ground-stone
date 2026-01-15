/**
 * Phase 2: 2025년 한국 세법 상수 정의
 */

// 2025년 소득세 누진세율표 (8단계)
export const TAX_BRACKETS_2025 = [
  { limit: 14000000, rate: 0.06, deduction: 0 },          // 1,400만원 이하: 6%
  { limit: 50000000, rate: 0.15, deduction: 1260000 },   // 5,000만원 이하: 15% - 126만원
  { limit: 88000000, rate: 0.24, deduction: 5760000 },   // 8,800만원 이하: 24% - 576만원
  { limit: 150000000, rate: 0.35, deduction: 15440000 }, // 1.5억원 이하: 35% - 1,544만원
  { limit: 300000000, rate: 0.38, deduction: 19940000 }, // 3억원 이하: 38% - 1,994만원
  { limit: 500000000, rate: 0.40, deduction: 25940000 }, // 5억원 이하: 40% - 2,594만원
  { limit: 1000000000, rate: 0.42, deduction: 35940000 }, // 10억원 이하: 42% - 3,594만원
  { limit: Infinity, rate: 0.45, deduction: 65940000 },   // 10억원 초과: 45% - 6,594만원
];

// 근로소득공제 구간 (5단계)
export const EARNED_INCOME_DEDUCTIONS = [
  { limit: 5000000, rate: 0.70, baseDeduction: 0 },        // 500만원 이하: 70%
  { limit: 15000000, rate: 0.40, baseDeduction: 1500000 }, // 1,500만원 이하: 40% + 150만원
  { limit: 45000000, rate: 0.15, baseDeduction: 5250000 }, // 4,500만원 이하: 15% + 525만원
  { limit: 100000000, rate: 0.05, baseDeduction: 9750000 }, // 1억원 이하: 5% + 975만원
  { limit: Infinity, rate: 0.02, baseDeduction: 12750000 }, // 1억원 초과: 2% + 1,275만원
];

// 근로소득공제 한도
export const EARNED_INCOME_DEDUCTION_LIMIT = 20000000; // 2,000만원

// 기본공제 (1인당)
export const BASIC_DEDUCTION_PER_PERSON = 1500000; // 150만원

// 추가공제
export const ADDITIONAL_DEDUCTIONS = {
  경로우대: 1000000,  // 70세 이상: 100만원
  장애인: 2000000,    // 장애인: 200만원
  부녀자: 500000,     // 부녀자: 50만원
  한부모: 1000000,    // 한부모: 100만원
};

// 의료비 공제
export const MEDICAL_EXPENSE = {
  총급여대비최소비율: 0.03,  // 총급여의 3% 초과분
  공제율: 0.15,               // 15% 공제
  한도: 7000000,              // 700만원 한도 (일반 의료비)
  노인장애인한도: Infinity,   // 65세 이상, 장애인은 한도 없음
};

// 2025년 자녀세액공제 (개정)
export const CHILD_TAX_CREDIT_2025 = [
  { children: 1, credit: 250000 },  // 1명: 25만원
  { children: 2, credit: 550000 },  // 2명: 55만원 (25 + 30)
  { children: 3, credit: 950000 },  // 3명: 95만원 (25 + 30 + 40)
];

// 3명 초과 시 추가 자녀 1명당
export const ADDITIONAL_CHILD_CREDIT = 400000; // 40만원

// 근로소득세액공제
export const EARNED_INCOME_TAX_CREDIT = {
  limit130: 1300000,   // 130만원 이하: 55% 공제
  rate55: 0.55,
  limit130_credit: 715000, // 130만원 이하 시 공제 한도: 71.5만원
  over130_base: 715000,    // 130만원 초과 시 기본: 71.5만원
  over130_rate: 0.30,      // 130만원 초과분의 30%
  maxCredit: 660000,       // 최대 공제액: 66만원
};
