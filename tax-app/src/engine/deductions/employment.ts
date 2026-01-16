/**
 * 근로소득공제 계산
 */

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
