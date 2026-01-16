/**
 * 한국 연말정산 계산 엔진
 * @module engine
 */

// 타입
export * from './types';

// 상수
export * from './constants';

// 메인 계산기
export { calculateYearEndTax } from './calculator';

// 공제 계산 함수들
export { calculateEmploymentIncome, calculateEmploymentIncomeDeduction } from './deductions/employment';
export { calculatePersonalDeduction } from './deductions/personal';
export { calculateCreditCardDeduction, suggestCreditCardOptimization } from './deductions/creditCard';
export { calculateMedicalCredit } from './deductions/medical';
export { calculateEducationCredit } from './deductions/education';
export { calculatePensionCredit } from './deductions/pension';
export { calculateRentCredit, calculateHousingLoanDeduction } from './deductions/housing';
export { calculateDonationCredit } from './deductions/donations';

// 시뮬레이션 & 추천
export { runSimulations, generateOptimizationSuggestions } from './simulator';
export { getPeerComparison } from './recommender';

// 검증
export { TaxInputValidator } from './validators';
