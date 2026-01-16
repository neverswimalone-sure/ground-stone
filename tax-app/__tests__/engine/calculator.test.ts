/**
 * 계산 엔진 단위 테스트
 */

import { calculateYearEndTax } from '../../src/engine/calculator';
import { TaxInputData } from '../../src/engine/types';

describe('연말정산 계산 엔진', () => {
  test('기본 케이스: 연봉 5천만원, 단순 입력', () => {
    const input: TaxInputData = {
      profile: {
        birthYear: 1990,
        isDisabled: false,
        isSingleParent: false,
      },
      income: {
        salary: 50_000_000,
        otherIncome: 0,
        withheldTax: 3_000_000,
      },
      dependents: [],
      creditCard: {
        creditCard: 10_000_000,
        checkCard: 5_000_000,
        cash: 0,
        traditionalMarket: 0,
        publicTransport: 1_000_000,
      },
      medical: {
        total: 0,
        elderlyOrDisabled: 0,
        infertility: 0,
      },
      education: {
        self: 0,
        children: {
          kindergarten: 0,
          elementary: 0,
          university: 0,
          disabled: 0,
        },
      },
      pension: {
        pensionSavings: 4_000_000,
        irp: 0,
      },
      housing: {
        type: 'none',
      },
      donation: {
        political: 0,
        religious: 0,
        general: 0,
      },
    };

    const result = calculateYearEndTax(input);

    // 기본 검증
    expect(result.totalIncome).toBe(50_000_000);
    expect(result.employmentIncomeDeduction).toBeGreaterThan(0);
    expect(result.refundOrPayment).toBeGreaterThan(0); // 환급 예상
  });

  test('복잡한 케이스: 부양가족 있음, 모든 공제 항목 존재', () => {
    const input: TaxInputData = {
      profile: {
        birthYear: 1985,
        isDisabled: false,
        isSingleParent: false,
      },
      income: {
        salary: 70_000_000,
        otherIncome: 0,
        withheldTax: 8_000_000,
      },
      dependents: [
        {
          id: '1',
          name: '배우자',
          relationship: '배우자',
          birthYear: 1987,
          isDisabled: false,
          annualIncome: 0,
          liveTogether: true,
        },
        {
          id: '2',
          name: '자녀1',
          relationship: '직계비속',
          birthYear: 2015,
          isDisabled: false,
          annualIncome: 0,
          liveTogether: true,
        },
      ],
      creditCard: {
        creditCard: 5_000_000,
        checkCard: 15_000_000,
        cash: 2_000_000,
        traditionalMarket: 2_000_000,
        publicTransport: 1_500_000,
      },
      medical: {
        total: 3_000_000,
        elderlyOrDisabled: 0,
        infertility: 0,
      },
      education: {
        self: 0,
        children: {
          kindergarten: 2_000_000,
          elementary: 0,
          university: 0,
          disabled: 0,
        },
      },
      pension: {
        pensionSavings: 4_000_000,
        irp: 3_000_000,
      },
      housing: {
        type: 'rent',
        monthlyRent: 600_000,
      },
      donation: {
        political: 0,
        religious: 1_000_000,
        general: 500_000,
      },
    };

    const result = calculateYearEndTax(input);

    // 검증
    expect(result.personalDeduction).toBe(4_500_000); // 본인 + 배우자 + 자녀 = 3 * 1,500,000
    expect(result.pensionCredit).toBeGreaterThan(0);
    expect(result.medicalCredit).toBeGreaterThan(0);
    expect(result.educationCredit).toBeGreaterThan(0);
  });

  test('엣지 케이스: 연봉 0원', () => {
    const input: TaxInputData = {
      profile: {
        birthYear: 1990,
        isDisabled: false,
        isSingleParent: false,
      },
      income: {
        salary: 0,
        otherIncome: 0,
        withheldTax: 0,
      },
      dependents: [],
      creditCard: {
        creditCard: 0,
        checkCard: 0,
        cash: 0,
        traditionalMarket: 0,
        publicTransport: 0,
      },
      medical: {
        total: 0,
        elderlyOrDisabled: 0,
        infertility: 0,
      },
      education: {
        self: 0,
        children: {
          kindergarten: 0,
          elementary: 0,
          university: 0,
          disabled: 0,
        },
      },
      pension: {
        pensionSavings: 0,
        irp: 0,
      },
      housing: {
        type: 'none',
      },
      donation: {
        political: 0,
        religious: 0,
        general: 0,
      },
    };

    const result = calculateYearEndTax(input);

    expect(result.determinedTax).toBe(0);
    expect(result.refundOrPayment).toBe(0);
  });
});
