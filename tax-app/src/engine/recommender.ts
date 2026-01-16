/**
 * 또래 비교 및 추천 엔진
 */

import { TaxInputData, TaxCalculationResult, PeerData } from './types';

// 샘플 데이터 (추후 실제 데이터로 교체)
const PEER_DATA: PeerData[] = [
  {
    salaryRange: '3000-4000',
    averagePensionPayment: 2_400_000,
    averageMedicalExpense: 800_000,
    averageCreditCardDeduction: 2_000_000,
    averageRefund: 280_000,
  },
  {
    salaryRange: '4000-5000',
    averagePensionPayment: 3_200_000,
    averageMedicalExpense: 1_000_000,
    averageCreditCardDeduction: 2_300_000,
    averageRefund: 380_000,
  },
  {
    salaryRange: '5000-7000',
    averagePensionPayment: 4_000_000,
    averageMedicalExpense: 1_200_000,
    averageCreditCardDeduction: 2_500_000,
    averageRefund: 520_000,
  },
  {
    salaryRange: '7000-10000',
    averagePensionPayment: 5_000_000,
    averageMedicalExpense: 1_500_000,
    averageCreditCardDeduction: 2_800_000,
    averageRefund: 680_000,
  },
];

/**
 * 연봉 구간 찾기
 */
function getSalaryRange(salary: number): string {
  const millions = Math.floor(salary / 10_000_000);
  const lower = millions * 1000;
  const upper = (millions + 1) * 1000;
  return `${lower}-${upper}`;
}

/**
 * 또래 비교 인사이트 생성
 */
export function getPeerComparison(
  input: TaxInputData,
  result: TaxCalculationResult
): {
  peerData: PeerData | null;
  insights: string[];
} {
  const range = getSalaryRange(input.income.salary);
  const peerData = PEER_DATA.find(p => p.salaryRange === range);

  if (!peerData) {
    return { peerData: null, insights: [] };
  }

  const insights: string[] = [];
  const userPension = input.pension.pensionSavings + input.pension.irp;

  // 연금 비교
  if (userPension < peerData.averagePensionPayment * 0.8) {
    const diff = Math.round((peerData.averagePensionPayment - userPension) / 10_000);
    insights.push(
      `💡 비슷한 연봉대의 평균 연금저축은 ${Math.round(peerData.averagePensionPayment / 10_000)}만원입니다. ` +
      `${diff}만원 더 납입하면 약 ${Math.round(diff * 0.165)}만원 환급 증가 예상`
    );
  }

  // 의료비 비교
  if (input.medical.total < peerData.averageMedicalExpense * 0.5) {
    insights.push(
      `💊 의료비 공제를 놓치셨을 수 있어요. 안경, 치과, 건강검진도 포함됩니다.`
    );
  }

  // 환급액 비교
  if (result.refundOrPayment < peerData.averageRefund * 0.7) {
    insights.push(
      `📊 비슷한 연봉대 평균 환급액은 ${Math.round(peerData.averageRefund / 10_000)}만원이에요. ` +
      `시뮬레이션으로 더 받을 방법을 찾아보세요!`
    );
  }

  return { peerData, insights };
}
