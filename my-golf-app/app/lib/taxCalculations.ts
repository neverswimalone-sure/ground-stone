/**
 * Phase 2: 핵심 계산 로직 5개 함수
 */

import {
  TAX_BRACKETS_2025,
  EARNED_INCOME_DEDUCTIONS,
  EARNED_INCOME_DEDUCTION_LIMIT,
  BASIC_DEDUCTION_PER_PERSON,
  ADDITIONAL_DEDUCTIONS,
  MEDICAL_EXPENSE,
} from './taxConstants';

/**
 * 함수 1: 근로소득공제 계산
 * 5단계 구간별 공제율 적용, 최대 2,000만원 한도
 */
export function calculateEarnedIncomeDeduction(총급여: number): number {
  let deduction = 0;

  for (const bracket of EARNED_INCOME_DEDUCTIONS) {
    if (총급여 <= bracket.limit) {
      deduction = 총급여 * bracket.rate + bracket.baseDeduction;
      break;
    }
  }

  // 한도 적용
  return Math.min(deduction, EARNED_INCOME_DEDUCTION_LIMIT);
}

/**
 * 함수 2: 인적공제 계산 (기본공제 + 추가공제)
 */
export function calculatePersonalDeductions(data: {
  본인포함부양가족수: number;
  경로우대자수: number;
  장애인수: number;
  부녀자공제: boolean;
  한부모공제: boolean;
}) {
  // 기본공제: 1인당 150만원
  const 기본공제 = data.본인포함부양가족수 * BASIC_DEDUCTION_PER_PERSON;

  // 추가공제
  let 추가공제 = 0;
  추가공제 += data.경로우대자수 * ADDITIONAL_DEDUCTIONS.경로우대;
  추가공제 += data.장애인수 * ADDITIONAL_DEDUCTIONS.장애인;
  if (data.부녀자공제) 추가공제 += ADDITIONAL_DEDUCTIONS.부녀자;
  if (data.한부모공제) 추가공제 += ADDITIONAL_DEDUCTIONS.한부모;

  return { 기본공제, 추가공제, 인적공제합계: 기본공제 + 추가공제 };
}

/**
 * 함수 3: 의료비공제 계산
 * 총급여의 3% 초과분에 대해 15% 공제, 일반 700만원 한도
 */
export function calculateMedicalDeduction(
  총급여: number,
  의료비지출액: number,
  노인장애인의료비: number
): number {
  const 최소기준 = 총급여 * MEDICAL_EXPENSE.총급여대비최소비율;

  // 일반 의료비 (3% 초과분, 700만원 한도)
  const 일반의료비초과분 = Math.max(0, 의료비지출액 - 최소기준);
  const 일반의료비공제대상 = Math.min(일반의료비초과분, MEDICAL_EXPENSE.한도);

  // 노인/장애인 의료비 (한도 없음)
  const 특수의료비공제대상 = 노인장애인의료비;

  // 총 공제액 (15%)
  const 총공제대상 = 일반의료비공제대상 + 특수의료비공제대상;
  return Math.floor(총공제대상 * MEDICAL_EXPENSE.공제율);
}

/**
 * 함수 4: 산출세액 계산 (8단계 누진세율 적용)
 */
export function calculateIncomeTax(과세표준: number): number {
  for (const bracket of TAX_BRACKETS_2025) {
    if (과세표준 <= bracket.limit) {
      return Math.floor(과세표준 * bracket.rate - bracket.deduction);
    }
  }
  return 0;
}

/**
 * 함수 5: 전체 세액 계산 (Phase 2 버전 - 세액공제 제외)
 */
export function calculateTax(formData: any) {
  // 1. 근로소득공제
  const 근로소득공제 = calculateEarnedIncomeDeduction(formData.총급여);
  const 근로소득금액 = formData.총급여 - 근로소득공제;

  // 2. 인적공제
  const { 기본공제, 추가공제, 인적공제합계 } = calculatePersonalDeductions({
    본인포함부양가족수: formData.본인포함부양가족수,
    경로우대자수: formData.경로우대자수,
    장애인수: formData.장애인수,
    부녀자공제: formData.부녀자공제,
    한부모공제: formData.한부모공제,
  });

  // 3. 기타 소득공제
  const 국민연금등 = formData.국민연금보험료 + formData.건강보험료;
  const 의료비공제 = calculateMedicalDeduction(
    formData.총급여,
    formData.의료비지출액,
    formData.노인장애인의료비
  );
  const 기타공제 = formData.기타특별소득공제;
  const 소득공제합계 = 인적공제합계 + 국민연금등 + 의료비공제 + 기타공제;

  // 4. 과세표준
  const 과세표준 = Math.max(0, 근로소득금액 - 소득공제합계);

  // 5. 산출세액
  const 산출세액 = calculateIncomeTax(과세표준);

  return {
    총급여: formData.총급여,
    근로소득공제,
    근로소득금액,
    기본공제,
    추가공제,
    인적공제합계,
    국민연금등,
    의료비공제,
    기타공제,
    소득공제합계,
    과세표준,
    산출세액,
    // Phase 3에서 추가 예정
    자녀세액공제: 0,
    근로소득세액공제: 0,
    세액공제합계: 0,
    결정세액: 산출세액, // Phase 3에서 세액공제 적용 후 계산
  };
}
