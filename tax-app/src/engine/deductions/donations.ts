/**
 * 기부금 세액공제 계산
 */

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
