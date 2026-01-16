/**
 * 한국 연말정산 계산 엔진 - 타입 정의
 * @version 1.0.0
 * @targetYear 2025
 */

/**
 * 사용자 기본 정보
 */
export interface UserProfile {
  birthYear: number;          // 출생연도
  isDisabled: boolean;        // 장애인 여부
  isSingleParent: boolean;    // 한부모 여부
}

/**
 * 소득 정보
 */
export interface IncomeData {
  salary: number;             // 총급여액 (비과세 제외)
  otherIncome: number;        // 기타소득
  withheldTax: number;        // 기납부 세액
}

/**
 * 부양가족 정보
 */
export interface Dependent {
  id: string;
  name: string;
  relationship: '배우자' | '직계존속' | '직계비속' | '형제자매' | '기타';
  birthYear: number;
  isDisabled: boolean;
  annualIncome: number;       // 연소득 (100만원 이하 확인)
  liveTogether: boolean;      // 동거 여부
}

/**
 * 신용카드 사용 내역
 */
export interface CreditCardData {
  creditCard: number;         // 신용카드 사용액
  checkCard: number;          // 체크카드 사용액
  cash: number;               // 현금영수증
  traditionalMarket: number;  // 전통시장
  publicTransport: number;    // 대중교통
}

/**
 * 의료비 지출
 */
export interface MedicalExpense {
  total: number;              // 총 의료비
  elderlyOrDisabled: number;  // 경로우대자/장애인
  infertility: number;        // 난임치료비
}

/**
 * 교육비 지출
 */
export interface EducationExpense {
  self: number;               // 본인 교육비
  children: {
    kindergarten: number;     // 취학전 아동
    elementary: number;       // 초중고
    university: number;       // 대학교
    disabled: number;         // 장애인 특수교육
  };
}

/**
 * 연금 납입
 */
export interface PensionPayment {
  pensionSavings: number;     // 연금저축
  irp: number;                // 퇴직연금(IRP)
}

/**
 * 주택 관련
 */
export interface HousingData {
  type: 'none' | 'rent' | 'loan';
  monthlyRent?: number;       // 월세액
  loanInterest?: number;      // 주택자금대출 이자
  isFirstHome?: boolean;      // 무주택자 여부
}

/**
 * 기부금
 */
export interface DonationData {
  political: number;          // 정치자금
  religious: number;          // 종교단체
  general: number;            // 일반 기부금
}

/**
 * 전체 입력 데이터
 */
export interface TaxInputData {
  profile: UserProfile;
  income: IncomeData;
  dependents: Dependent[];
  creditCard: CreditCardData;
  medical: MedicalExpense;
  education: EducationExpense;
  pension: PensionPayment;
  housing: HousingData;
  donation: DonationData;
}

/**
 * 계산 결과
 */
export interface TaxCalculationResult {
  // 소득 단계
  totalIncome: number;                    // 총급여
  employmentIncomeDeduction: number;      // 근로소득공제
  employmentIncome: number;               // 근로소득금액

  // 공제 단계
  personalDeduction: number;              // 인적공제
  creditCardDeduction: number;            // 신용카드 소득공제
  pensionDeduction: number;               // 연금보험료 소득공제
  housingDeduction: number;               // 주택자금 소득공제
  totalIncomeDeduction: number;           // 소득공제 합계

  taxableIncome: number;                  // 과세표준

  // 세액 단계
  calculatedTax: number;                  // 산출세액

  medicalCredit: number;                  // 의료비 세액공제
  educationCredit: number;                // 교육비 세액공제
  pensionCredit: number;                  // 연금저축 세액공제
  donationCredit: number;                 // 기부금 세액공제
  creditCardCredit: number;               // 신용카드 세액공제 (2025년 신설)
  totalTaxCredit: number;                 // 세액공제 합계

  determinedTax: number;                  // 결정세액
  withheldTax: number;                    // 기납부세액

  // 최종 결과
  refundOrPayment: number;                // 환급/납부세액 (양수: 환급, 음수: 납부)

  // 메타 정보
  effectiveTaxRate: number;               // 실효세율
  calculatedAt: Date;
}

/**
 * 검증 결과
 */
export interface ValidationResult {
  valid: boolean;
  error?: string;
  warnings?: string[];
}

/**
 * 시뮬레이션 시나리오
 */
export interface SimulationScenario {
  id: string;
  name: string;
  description: string;
  changes: Partial<TaxInputData>;
  impact: number;                // 환급액 변화 (양수: 증가, 음수: 감소)
}

/**
 * 또래 비교 데이터
 */
export interface PeerData {
  salaryRange: string;
  averagePensionPayment: number;
  averageMedicalExpense: number;
  averageCreditCardDeduction: number;
  averageRefund: number;
}
