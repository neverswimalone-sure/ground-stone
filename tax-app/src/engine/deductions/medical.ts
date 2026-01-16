/**
 * 의료비 세액공제 계산
 */

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
