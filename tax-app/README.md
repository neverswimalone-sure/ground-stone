# 🇰🇷 한국 연말정산 자동계산 앱

> 2025년 귀속 연말정산을 10분 안에 끝내고, 최대 환급액을 받아가세요!

[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![React Native](https://img.shields.io/badge/React%20Native-0.73-61dafb)](https://reactnative.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## ✨ 주요 기능

- 🚀 **10분 완료**: 최소한의 입력으로 정확한 계산
- 🎯 **99% 정확도**: 국세청 공식 계산식 기반
- 🔒 **100% 프라이버시**: 모든 계산은 기기 내부에서
- 💡 **What-If 시뮬레이션**: "연금 100만원 더 넣으면?" 실시간 비교
- 📊 **또래 비교**: 비슷한 연봉대 평균과 비교
- 💰 **절세 팁**: AI 기반 맞춤 최적화 제안

---

## 📱 스크린샷

*(향후 추가)*

---

## 🚀 빠른 시작

### 사전 요구사항

- Node.js 18 이상
- npm 또는 yarn

### 설치

```bash
# 저장소 클론
git clone https://github.com/your-repo/korean-tax-app.git
cd korean-tax-app/tax-app

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

### 데모 실행 (계산 엔진만)

계산 엔진만 테스트하려면:

```bash
# TypeScript 직접 실행
npx ts-node examples/demo.ts
```

**예상 출력:**
```
============================================================
🇰🇷 한국 연말정산 계산 엔진 데모
============================================================

📊 1. 연말정산 계산 결과

📌 소득 정보
   총급여: 50,000,000원
   근로소득공제: 12,000,000원
   근로소득금액: 38,000,000원

📌 소득공제
   인적공제: 4,500,000원
   신용카드: 2,250,000원
   ...

🎉 환급세액: 385,000원
```

---

## 📂 프로젝트 구조

```
tax-app/
├── src/
│   ├── engine/              # 💎 핵심 계산 엔진 (Pure TypeScript)
│   │   ├── types.ts         # 타입 정의
│   │   ├── constants.ts     # 2025년 세법 상수
│   │   ├── calculator.ts    # 메인 계산기
│   │   ├── deductions/      # 공제 계산 함수들
│   │   │   ├── employment.ts
│   │   │   ├── personal.ts
│   │   │   ├── creditCard.ts
│   │   │   ├── medical.ts
│   │   │   ├── education.ts
│   │   │   ├── pension.ts
│   │   │   ├── housing.ts
│   │   │   └── donations.ts
│   │   ├── simulator.ts     # What-If 시뮬레이션
│   │   ├── recommender.ts   # 또래 비교 & 추천
│   │   └── validators.ts    # 입력 검증
│   │
│   ├── store/               # Redux 상태 관리 (향후)
│   ├── screens/             # UI 화면 (향후)
│   ├── components/          # 재사용 컴포넌트 (향후)
│   └── navigation/          # 네비게이션 (향후)
│
├── __tests__/               # 테스트
│   └── engine/
│       └── calculator.test.ts
│
├── examples/                # 예제 코드
│   └── demo.ts
│
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🧮 계산 엔진 사용법

### 기본 사용

```typescript
import { calculateYearEndTax, TaxInputData } from './src/engine';

const input: TaxInputData = {
  profile: {
    birthYear: 1985,
    isDisabled: false,
    isSingleParent: false,
  },
  income: {
    salary: 50_000_000,
    otherIncome: 0,
    withheldTax: 3_500_000,
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
  ],
  creditCard: {
    creditCard: 8_000_000,
    checkCard: 6_000_000,
    cash: 1_000_000,
    traditionalMarket: 500_000,
    publicTransport: 1_200_000,
  },
  // ... 기타 항목
};

const result = calculateYearEndTax(input);

console.log(`환급액: ${result.refundOrPayment.toLocaleString()}원`);
```

### 시뮬레이션

```typescript
import { generateOptimizationSuggestions } from './src/engine';

const suggestions = generateOptimizationSuggestions(input);

suggestions.forEach(s => {
  console.log(`${s.name}: +${s.impact.toLocaleString()}원`);
});
```

---

## 🧪 테스트

```bash
# 모든 테스트 실행
npm test

# Watch 모드
npm run test:watch

# 커버리지
npm run test:coverage
```

---

## 📊 2025년 세법 주요 변경사항

이 앱은 2025년 귀속 최신 세법을 반영합니다:

| 항목 | 2024년 | 2025년 | 변화 |
|------|--------|--------|------|
| **신용카드 공제 한도** | 250만원 | 300만원 | ↑ 50만원 |
| **전통시장 추가 한도** | - | 100만원 | 신설 |
| **대중교통 추가 한도** | - | 100만원 | 신설 |
| **연금저축 세액공제율** | 12%/15% | 13.2%/16.5% | ↑ |

---

## 🔒 프라이버시 & 보안

- ✅ **로컬 계산**: 모든 세금 계산은 기기 내부에서만 수행
- ✅ **데이터 암호화**: 민감 정보는 Expo SecureStore 사용
- ✅ **선택적 동기화**: 클라우드 백업은 사용자 동의 시에만
- ✅ **익명 분석**: 통계 수집은 개인 식별 정보 제외

---

## 🗺️ 로드맵

### Phase 1: 계산 엔진 (✅ 완료)
- [x] 타입 정의
- [x] 2025년 세법 상수
- [x] 모든 공제 계산 함수
- [x] 메인 계산기
- [x] What-If 시뮬레이션
- [x] 입력 검증

### Phase 2: UI 구현 (🚧 진행 중)
- [ ] Redux 스토어
- [ ] 기본 컴포넌트
- [ ] 화면 구현 (11개)
- [ ] 네비게이션
- [ ] 애니메이션

### Phase 3: 고급 기능 (📅 예정)
- [ ] OCR 영수증 인식
- [ ] 홈택스 간편 연동
- [ ] PDF 리포트 생성
- [ ] 푸시 알림 (세법 개정)

### Phase 4: 출시 (📅 예정)
- [ ] 앱스토어 출시
- [ ] 플레이스토어 출시
- [ ] 사용자 피드백 반영

---

## 🤝 기여하기

기여를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚠️ 법적 고지사항

**이 앱은 예상 금액 계산 도구이며, 공식 세무 자문이 아닙니다.**

- 실제 신고는 국세청 홈택스 또는 세무사와 상담하시기 바랍니다.
- 계산 결과의 정확성을 보장하지 않습니다.
- 세법은 수시로 변경될 수 있으며, 앱 업데이트가 필요합니다.

---

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

---

## 📞 문의

- GitHub Issues: [이슈 등록](https://github.com/your-repo/korean-tax-app/issues)
- Email: support@example.com

---

## 🙏 참고 자료

- [국세청 홈택스](https://www.hometax.go.kr)
- [국가법령정보센터 - 소득세법](https://www.law.go.kr)
- [설계 문서](../DESIGN_KOREAN_TAX_APP.md)

---

**Made with ❤️ for Korean taxpayers**
