/**
 * 연금저축 세액공제 계산
 */

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
