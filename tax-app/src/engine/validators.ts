/**
 * 입력 검증 로직
 */

import { VALIDATION, PERSONAL_DEDUCTION } from './constants';
import { Dependent, CreditCardData, ValidationResult } from './types';

/**
 * 세금 입력 검증 클래스
 */
export class TaxInputValidator {
  /**
   * 연봉 검증
   */
  static validateSalary(salary: number): ValidationResult {
    if (salary < VALIDATION.MIN_SALARY) {
      return { valid: false, error: '연봉은 0원 이상이어야 합니다' };
    }
    if (salary > VALIDATION.MAX_SALARY) {
      return { valid: false, error: '연봉이 비현실적으로 높습니다 (최대 10억)' };
    }
    return { valid: true };
  }

  /**
   * 부양가족 검증
   */
  static validateDependents(dependents: Dependent[]): ValidationResult {
    if (dependents.length > VALIDATION.MAX_DEPENDENTS) {
      return { valid: false, error: '부양가족이 너무 많습니다 (최대 20명)' };
    }

    // 중복 확인
    const names = dependents.map(d => d.name);
    const uniqueNames = new Set(names);
    if (names.length !== uniqueNames.size) {
      return { valid: false, error: '중복된 부양가족이 있습니다' };
    }

    const warnings: string[] = [];

    // 소득 초과자 경고
    for (const dependent of dependents) {
      if (dependent.annualIncome > PERSONAL_DEDUCTION.INCOME_LIMIT) {
        warnings.push(`${dependent.name}님은 소득이 100만원을 초과하여 공제 대상이 아닙니다`);
      }
    }

    return { valid: true, warnings: warnings.length > 0 ? warnings : undefined };
  }

  /**
   * 신용카드 사용액 검증
   */
  static validateCreditCard(
    salary: number,
    cardData: CreditCardData
  ): ValidationResult {
    const total =
      cardData.creditCard +
      cardData.checkCard +
      cardData.cash +
      cardData.traditionalMarket +
      cardData.publicTransport;

    // 음수 검증
    if (Object.values(cardData).some(v => v < 0)) {
      return { valid: false, error: '음수 값은 입력할 수 없습니다' };
    }

    // 연봉의 3배 초과 시 경고
    if (total > salary * 3) {
      return {
        valid: false,
        error: '카드 사용액이 연봉의 3배를 초과합니다. 입력을 확인해주세요.'
      };
    }

    return { valid: true };
  }

  /**
   * 의료비 검증
   */
  static validateMedical(total: number, special: number): ValidationResult {
    if (total < 0 || special < 0) {
      return { valid: false, error: '음수 값은 입력할 수 없습니다' };
    }

    if (special > total) {
      return { valid: false, error: '특수 의료비가 총 의료비보다 클 수 없습니다' };
    }

    return { valid: true };
  }

  /**
   * 연금 납입액 검증
   */
  static validatePension(pension: number, irp: number): ValidationResult {
    if (pension < 0 || irp < 0) {
      return { valid: false, error: '음수 값은 입력할 수 없습니다' };
    }

    const total = pension + irp;
    if (total > 20_000_000) {
      return {
        valid: false,
        error: '연금 납입액이 비현실적으로 높습니다',
        warnings: ['연금저축+IRP 합산 한도는 900만원입니다']
      };
    }

    return { valid: true };
  }
}
