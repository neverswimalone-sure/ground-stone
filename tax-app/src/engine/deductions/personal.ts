/**
 * 인적공제 계산
 */

import { PERSONAL_DEDUCTION, TAX_YEAR } from '../constants';
import { Dependent, UserProfile } from '../types';

/**
 * 나이 확인 (기준: 2025년 12월 31일)
 */
function getAge(birthYear: number): number {
  return TAX_YEAR.TARGET_YEAR - birthYear + 1; // 만 나이
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
