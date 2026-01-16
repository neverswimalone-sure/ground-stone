/**
 * What-If 시뮬레이션 엔진
 */

import { TaxInputData, TaxCalculationResult, SimulationScenario } from './types';
import { calculateYearEndTax } from './calculator';

/**
 * What-If 시뮬레이션 실행
 *
 * @param baseInput 기본 입력 데이터
 * @param scenarios 시뮬레이션할 시나리오들
 * @returns 각 시나리오별 결과
 */
export function runSimulations(
  baseInput: TaxInputData,
  scenarios: Partial<TaxInputData>[]
): Array<{
  scenario: Partial<TaxInputData>;
  result: TaxCalculationResult;
  improvement: number;
}> {
  const baseResult = calculateYearEndTax(baseInput);

  return scenarios.map(scenario => {
    const modifiedInput: TaxInputData = {
      ...baseInput,
      ...scenario,
      // 중첩 객체 병합
      pension: { ...baseInput.pension, ...scenario.pension },
      creditCard: { ...baseInput.creditCard, ...scenario.creditCard },
      medical: { ...baseInput.medical, ...scenario.medical },
      education: { ...baseInput.education, ...scenario.education },
      housing: { ...baseInput.housing, ...scenario.housing },
      donation: { ...baseInput.donation, ...scenario.donation },
    };

    const result = calculateYearEndTax(modifiedInput);
    const improvement = result.refundOrPayment - baseResult.refundOrPayment;

    return { scenario, result, improvement };
  });
}

/**
 * 자동 최적화 제안 생성
 */
export function generateOptimizationSuggestions(
  input: TaxInputData
): SimulationScenario[] {
  const suggestions: SimulationScenario[] = [];
  const baseResult = calculateYearEndTax(input);

  // 1. 연금저축 증액 시뮬레이션
  const currentPension = input.pension.pensionSavings + input.pension.irp;
  if (currentPension < 6_000_000) {
    const increasePension = 1_000_000; // 100만원 증액
    const modifiedInput = {
      ...input,
      pension: {
        ...input.pension,
        pensionSavings: input.pension.pensionSavings + increasePension,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'pension-increase',
      name: '연금저축 100만원 추가',
      description: `올해 연금저축을 ${Math.round(increasePension / 10_000)}만원 더 납입하면`,
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 2. 신용카드 → 체크카드 전환
  if (input.creditCard.creditCard > input.creditCard.checkCard) {
    const modifiedInput = {
      ...input,
      creditCard: {
        ...input.creditCard,
        checkCard: input.creditCard.creditCard + input.creditCard.checkCard,
        creditCard: 0,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'card-switch',
      name: '신용카드 → 체크카드',
      description: '내년에 신용카드 대신 체크카드를 쓰면',
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 3. 전통시장 이용 증가
  if (input.creditCard.traditionalMarket < 2_000_000) {
    const increase = 500_000; // 50만원 증액
    const modifiedInput = {
      ...input,
      creditCard: {
        ...input.creditCard,
        traditionalMarket: input.creditCard.traditionalMarket + increase,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'traditional-market',
      name: '전통시장 50만원 더 이용',
      description: '전통시장 사용액을 늘리면 (40% 공제율)',
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 4. IRP 추가 납입 (연금저축 + IRP 합산 한도)
  const totalPension = input.pension.pensionSavings + input.pension.irp;
  if (totalPension < 9_000_000 && input.pension.irp < 3_000_000) {
    const modifiedInput = {
      ...input,
      pension: {
        ...input.pension,
        irp: input.pension.irp + 1_000_000,
      },
    };
    const result = calculateYearEndTax(modifiedInput);

    suggestions.push({
      id: 'irp-increase',
      name: 'IRP 100만원 추가',
      description: '퇴직연금(IRP)을 추가로 납입하면',
      changes: modifiedInput,
      impact: result.refundOrPayment - baseResult.refundOrPayment,
    });
  }

  // 영향도 높은 순으로 정렬
  return suggestions
    .filter(s => s.impact > 10_000) // 1만원 이상 효과만
    .sort((a, b) => b.impact - a.impact);
}
