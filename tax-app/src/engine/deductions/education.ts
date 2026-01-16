/**
 * 교육비 세액공제 계산
 */

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
