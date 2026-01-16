/**
 * 주택 관련 공제 계산
 */

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
