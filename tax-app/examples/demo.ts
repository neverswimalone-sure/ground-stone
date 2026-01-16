/**
 * 연말정산 계산 엔진 데모
 *
 * 이 파일을 실행하면 실제 계산 결과를 확인할 수 있습니다.
 *
 * 실행 방법:
 * ```bash
 * npx ts-node examples/demo.ts
 * ```
 */

import {
  calculateYearEndTax,
  generateOptimizationSuggestions,
  getPeerComparison,
  TaxInputData,
} from '../src/engine';

// 샘플 데이터: 연봉 5천만원, 배우자 + 자녀 1명
const sampleInput: TaxInputData = {
  profile: {
    birthYear: 1985,
    isDisabled: false,
    isSingleParent: false,
  },
  income: {
    salary: 50_000_000,
    otherIncome: 0,
    withheldTax: 3_500_000, // 기납부 세액
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
      name: '자녀',
      relationship: '직계비속',
      birthYear: 2015,
      isDisabled: false,
      annualIncome: 0,
      liveTogether: true,
    },
  ],
  creditCard: {
    creditCard: 8_000_000,   // 신용카드
    checkCard: 6_000_000,    // 체크카드
    cash: 1_000_000,         // 현금영수증
    traditionalMarket: 500_000, // 전통시장
    publicTransport: 1_200_000, // 대중교통
  },
  medical: {
    total: 2_000_000,
    elderlyOrDisabled: 0,
    infertility: 0,
  },
  education: {
    self: 0,
    children: {
      kindergarten: 1_500_000, // 유치원
      elementary: 0,
      university: 0,
      disabled: 0,
    },
  },
  pension: {
    pensionSavings: 3_000_000, // 연금저축
    irp: 2_000_000,            // IRP
  },
  housing: {
    type: 'rent',
    monthlyRent: 500_000, // 월세 50만원
  },
  donation: {
    political: 0,
    religious: 500_000,
    general: 300_000,
  },
};

console.log('='.repeat(60));
console.log('🇰🇷 한국 연말정산 계산 엔진 데모');
console.log('='.repeat(60));

// 1. 기본 계산
console.log('\n📊 1. 연말정산 계산 결과\n');
const result = calculateYearEndTax(sampleInput);

console.log(`📌 소득 정보`);
console.log(`   총급여: ${result.totalIncome.toLocaleString()}원`);
console.log(`   근로소득공제: ${result.employmentIncomeDeduction.toLocaleString()}원`);
console.log(`   근로소득금액: ${result.employmentIncome.toLocaleString()}원`);

console.log(`\n📌 소득공제`);
console.log(`   인적공제: ${result.personalDeduction.toLocaleString()}원`);
console.log(`   신용카드: ${result.creditCardDeduction.toLocaleString()}원`);
console.log(`   연금보험료: ${result.pensionDeduction.toLocaleString()}원`);
console.log(`   소득공제 합계: ${result.totalIncomeDeduction.toLocaleString()}원`);

console.log(`\n📌 과세표준 및 산출세액`);
console.log(`   과세표준: ${result.taxableIncome.toLocaleString()}원`);
console.log(`   산출세액: ${result.calculatedTax.toLocaleString()}원`);

console.log(`\n📌 세액공제`);
console.log(`   의료비: ${result.medicalCredit.toLocaleString()}원`);
console.log(`   교육비: ${result.educationCredit.toLocaleString()}원`);
console.log(`   연금저축: ${result.pensionCredit.toLocaleString()}원`);
console.log(`   기부금: ${result.donationCredit.toLocaleString()}원`);
console.log(`   세액공제 합계: ${result.totalTaxCredit.toLocaleString()}원`);

console.log(`\n📌 최종 결과`);
console.log(`   결정세액: ${result.determinedTax.toLocaleString()}원`);
console.log(`   기납부세액: ${result.withheldTax.toLocaleString()}원`);
console.log(`   실효세율: ${result.effectiveTaxRate.toFixed(2)}%`);

if (result.refundOrPayment > 0) {
  console.log(`\n🎉 환급세액: ${result.refundOrPayment.toLocaleString()}원`);
} else {
  console.log(`\n💸 추가납부세액: ${Math.abs(result.refundOrPayment).toLocaleString()}원`);
}

// 2. 최적화 제안
console.log('\n' + '='.repeat(60));
console.log('💡 2. 절세 최적화 제안\n');

const suggestions = generateOptimizationSuggestions(sampleInput);

if (suggestions.length === 0) {
  console.log('   이미 최적화되어 있습니다! 👍');
} else {
  suggestions.forEach((suggestion, index) => {
    console.log(`${index + 1}. ${suggestion.name}`);
    console.log(`   ${suggestion.description}`);
    console.log(`   💰 예상 환급 증가: ${Math.round(suggestion.impact).toLocaleString()}원\n`);
  });
}

// 3. 또래 비교
console.log('='.repeat(60));
console.log('📊 3. 또래 비교\n');

const { peerData, insights } = getPeerComparison(sampleInput, result);

if (peerData) {
  console.log(`연봉 구간: ${peerData.salaryRange.replace('-', '~')}만원`);
  console.log(`평균 연금저축: ${Math.round(peerData.averagePensionPayment / 10_000)}만원`);
  console.log(`평균 환급액: ${Math.round(peerData.averageRefund / 10_000)}만원\n`);

  if (insights.length > 0) {
    console.log('인사이트:');
    insights.forEach(insight => console.log(`  ${insight}`));
  }
} else {
  console.log('또래 비교 데이터가 없습니다.');
}

console.log('\n' + '='.repeat(60));
console.log('✅ 계산 완료!');
console.log('='.repeat(60));
