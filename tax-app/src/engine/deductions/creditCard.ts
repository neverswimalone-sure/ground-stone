/**
 * 신용카드 소득공제 계산 (2025년 개정)
 */

import { CREDIT_CARD_DEDUCTION } from '../constants';
import { CreditCardData } from '../types';

/**
 * 신용카드 소득공제 계산 (2025년 개정)
 *
 * 주요 변경사항:
 * - 기본 한도: 250만원 → 300만원 상향
 * - 전통시장/대중교통 각 100만원 추가 한도
 *
 * @param salary 총급여액
 * @param cardData 신용카드 사용 데이터
 * @returns 신용카드 소득공제액
 */
export function calculateCreditCardDeduction(
  salary: number,
  cardData: CreditCardData
): number {
  // 1. 최저사용금액 (총급여의 25%)
  const threshold = salary * CREDIT_CARD_DEDUCTION.THRESHOLD_RATE;

  // 2. 총 사용액
  const totalSpend =
    cardData.creditCard +
    cardData.checkCard +
    cardData.cash +
    cardData.traditionalMarket +
    cardData.publicTransport;

  // 최저사용금액 미달 시 공제 없음
  if (totalSpend <= threshold) {
    return 0;
  }

  // 3. 공제대상 금액 (순서대로 차감)
  let remaining = totalSpend - threshold;
  let deduction = 0;

  // 3-1. 신용카드 (15%, 가장 낮은 공제율이므로 먼저 차감)
  const creditUsed = Math.min(remaining, cardData.creditCard);
  deduction += creditUsed * CREDIT_CARD_DEDUCTION.RATES.CREDIT;
  remaining -= creditUsed;

  // 3-2. 체크카드/현금 (30%)
  const checkCashTotal = cardData.checkCard + cardData.cash;
  const checkCashUsed = Math.min(remaining, checkCashTotal);
  deduction += checkCashUsed * CREDIT_CARD_DEDUCTION.RATES.CHECK;
  remaining -= checkCashUsed;

  // 3-3. 전통시장 (40%, 추가한도 별도)
  const marketUsed = Math.min(remaining, cardData.traditionalMarket);
  const marketDeduction = marketUsed * CREDIT_CARD_DEDUCTION.RATES.TRADITIONAL_MARKET;
  deduction += marketDeduction;
  remaining -= marketUsed;

  // 3-4. 대중교통 (40%, 추가한도 별도)
  const transportUsed = Math.min(remaining, cardData.publicTransport);
  const transportDeduction = transportUsed * CREDIT_CARD_DEDUCTION.RATES.PUBLIC_TRANSPORT;
  deduction += transportDeduction;

  // 4. 한도 적용
  let limit = CREDIT_CARD_DEDUCTION.LIMITS.BASE;

  // 전통시장 추가한도 (최대 100만원 추가 공제)
  const marketExtraDeduction = Math.min(
    marketDeduction,
    CREDIT_CARD_DEDUCTION.LIMITS.TRADITIONAL_EXTRA
  );
  limit += marketExtraDeduction;

  // 대중교통 추가한도 (최대 100만원 추가 공제)
  const transportExtraDeduction = Math.min(
    transportDeduction,
    CREDIT_CARD_DEDUCTION.LIMITS.TRANSPORT_EXTRA
  );
  limit += transportExtraDeduction;

  // 소득 구간별 한도 조정 (7천만원 초과 시 한도 감소)
  if (salary > CREDIT_CARD_DEDUCTION.SALARY_THRESHOLD) {
    limit = Math.min(limit, CREDIT_CARD_DEDUCTION.LIMITS.BASE * 0.5); // 50% 감소
  }

  return Math.min(deduction, limit);
}

/**
 * 신용카드 공제 최적화 시뮬레이션
 *
 * @param salary 총급여액
 * @param currentCardData 현재 사용 패턴
 * @returns 최적화 제안
 */
export function suggestCreditCardOptimization(
  salary: number,
  currentCardData: CreditCardData
): {
  currentDeduction: number;
  maxPossibleDeduction: number;
  suggestions: string[];
} {
  const current = calculateCreditCardDeduction(salary, currentCardData);
  const suggestions: string[] = [];

  // 체크카드 비중 증가 제안
  if (currentCardData.creditCard > currentCardData.checkCard) {
    const optimizedData: CreditCardData = {
      ...currentCardData,
      checkCard: currentCardData.creditCard + currentCardData.checkCard,
      creditCard: 0,
    };
    const optimized = calculateCreditCardDeduction(salary, optimizedData);
    const increase = optimized - current;

    if (increase > 10_000) {
      suggestions.push(
        `신용카드 대신 체크카드 사용 시 약 ${Math.round(increase / 10_000)}만원 추가 공제`
      );
    }
  }

  // 전통시장 사용 제안
  if (currentCardData.traditionalMarket < 1_000_000) {
    suggestions.push(
      `전통시장에서 ${Math.round((1_000_000 - currentCardData.traditionalMarket) / 10_000)}만원 더 사용하면 최대 공제 가능`
    );
  }

  return {
    currentDeduction: current,
    maxPossibleDeduction: CREDIT_CARD_DEDUCTION.LIMITS.BASE +
                          CREDIT_CARD_DEDUCTION.LIMITS.TRADITIONAL_EXTRA +
                          CREDIT_CARD_DEDUCTION.LIMITS.TRANSPORT_EXTRA,
    suggestions,
  };
}
