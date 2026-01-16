/**
 * 메인 연말정산 계산 엔진
 */

import { TAX_BRACKETS } from './constants';
import { TaxInputData, TaxCalculationResult } from './types';
import { calculateEmploymentIncome, calculateEmploymentIncomeDeduction } from './deductions/employment';
import { calculatePersonalDeduction } from './deductions/personal';
import { calculateCreditCardDeduction } from './deductions/creditCard';
import { calculateMedicalCredit } from './deductions/medical';
import { calculateEducationCredit } from './deductions/education';
import { calculatePensionCredit } from './deductions/pension';
import { calculateRentCredit, calculateHousingLoanDeduction } from './deductions/housing';
import { calculateDonationCredit } from './deductions/donations';

/**
 * 과세표준별 산출세액 계산
 */
function calculateTaxFromBracket(taxableIncome: number): number {
  for (const bracket of TAX_BRACKETS) {
    if (taxableIncome <= bracket.max) {
      return taxableIncome * bracket.rate - bracket.deduction;
    }
  }
  return 0;
}

/**
 * 메인 연말정산 계산 엔진
 *
 * @param input 사용자 입력 데이터
 * @returns 계산 결과
 */
export function calculateYearEndTax(input: TaxInputData): TaxCalculationResult {
  const { profile, income, dependents, creditCard, medical, education, pension, housing, donation } = input;

  // ===== 1단계: 소득 =====
  const totalIncome = income.salary + income.otherIncome;
  const employmentIncomeDeduction = calculateEmploymentIncomeDeduction(income.salary);
  const employmentIncome = calculateEmploymentIncome(income.salary);

  // ===== 2단계: 소득공제 =====
  const personalDeduction = calculatePersonalDeduction(profile, dependents);
  const creditCardDeduction = calculateCreditCardDeduction(income.salary, creditCard);

  // 연금보험료 소득공제 (국민연금 등, 납입액 전액)
  const pensionDeduction = pension.pensionSavings + pension.irp;

  // 주택자금 소득공제
  const housingDeduction = housing.type === 'loan' && housing.loanInterest
    ? calculateHousingLoanDeduction(housing.loanInterest)
    : 0;

  const totalIncomeDeduction =
    personalDeduction +
    creditCardDeduction +
    pensionDeduction +
    housingDeduction;

  // ===== 3단계: 과세표준 =====
  const taxableIncome = Math.max(0, employmentIncome - totalIncomeDeduction);

  // ===== 4단계: 산출세액 =====
  const calculatedTax = calculateTaxFromBracket(taxableIncome);

  // ===== 5단계: 세액공제 =====
  const medicalCredit = calculateMedicalCredit(income.salary, medical);
  const educationCredit = calculateEducationCredit(education);
  const pensionCredit = calculatePensionCredit(income.salary, pension);
  const donationCredit = calculateDonationCredit(employmentIncome, donation);

  // 월세 세액공제
  const rentCredit = housing.type === 'rent' && housing.monthlyRent
    ? calculateRentCredit(income.salary, housing.monthlyRent)
    : 0;

  // 신용카드 세액공제 (2025년 추가 고려 - 실제로는 소득공제로만 존재)
  const creditCardCredit = 0;

  const totalTaxCredit =
    medicalCredit +
    educationCredit +
    pensionCredit +
    donationCredit +
    rentCredit +
    creditCardCredit;

  // ===== 6단계: 결정세액 =====
  const determinedTax = Math.max(0, calculatedTax - totalTaxCredit);

  // ===== 7단계: 환급/납부 =====
  const refundOrPayment = income.withheldTax - determinedTax;

  // ===== 실효세율 =====
  const effectiveTaxRate = totalIncome > 0 ? (determinedTax / totalIncome) * 100 : 0;

  return {
    totalIncome,
    employmentIncomeDeduction,
    employmentIncome,
    personalDeduction,
    creditCardDeduction,
    pensionDeduction,
    housingDeduction,
    totalIncomeDeduction,
    taxableIncome,
    calculatedTax,
    medicalCredit,
    educationCredit,
    pensionCredit,
    donationCredit,
    creditCardCredit,
    totalTaxCredit,
    determinedTax,
    withheldTax: income.withheldTax,
    refundOrPayment,
    effectiveTaxRate,
    calculatedAt: new Date(),
  };
}
