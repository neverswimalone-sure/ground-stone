'use client';

import { useState } from 'react';

// Phase 1: UI 프레임만 구성 (계산 로직은 Phase 2에서)
export default function Home() {
  const [formData, setFormData] = useState({
    총급여: 50000000,
    본인포함부양가족수: 3,
    경로우대자수: 0,
    장애인수: 0,
    부녀자공제: false,
    한부모공제: false,
    자녀수: 2,
    국민연금보험료: 2000000,
    건강보험료: 1500000,
    의료비지출액: 2000000,
    노인장애인의료비: 0,
    기타특별소득공제: 0,
  });

  const [showResult, setShowResult] = useState(false);

  const handleCalculate = () => {
    // Phase 2에서 계산 로직 연결
    setShowResult(true);
  };

  const updateField = (field: string, value: number | boolean) => {
    setFormData({ ...formData, [field]: value });
    setShowResult(false);
  };

  const formatNumber = (value: number) => {
    return value.toLocaleString('ko-KR') + '원';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* 헤더 */}
        <header className="text-center mb-10">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            💰 2025 연말정산 계산기
          </h1>
          <p className="text-gray-600">
            2025년 개정 세법 반영 (8단계 누진세율, 자녀세액공제 개정)
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-8">
          {/* 왼쪽: 입력 폼 */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6 border-b pb-3">
              📝 정보 입력
            </h2>

            <div className="space-y-6">
              {/* 소득 정보 */}
              <FormSection title="소득 정보">
                <NumberInput
                  label="총급여"
                  value={formData.총급여}
                  onChange={(v) => updateField('총급여', v)}
                  placeholder="예: 50,000,000"
                />
              </FormSection>

              {/* 인적공제 */}
              <FormSection title="인적공제">
                <NumberInput
                  label="본인 포함 부양가족 수"
                  value={formData.본인포함부양가족수}
                  onChange={(v) => updateField('본인포함부양가족수', v)}
                  suffix="명"
                />
                <NumberInput
                  label="경로우대 (70세 이상)"
                  value={formData.경로우대자수}
                  onChange={(v) => updateField('경로우대자수', v)}
                  suffix="명"
                />
                <NumberInput
                  label="장애인"
                  value={formData.장애인수}
                  onChange={(v) => updateField('장애인수', v)}
                  suffix="명"
                />
                <CheckboxInput
                  label="부녀자 공제"
                  checked={formData.부녀자공제}
                  onChange={(v) => updateField('부녀자공제', v)}
                />
                <CheckboxInput
                  label="한부모 공제"
                  checked={formData.한부모공제}
                  onChange={(v) => updateField('한부모공제', v)}
                />
              </FormSection>

              {/* 자녀 정보 */}
              <FormSection title="자녀 정보">
                <NumberInput
                  label="자녀 수"
                  value={formData.자녀수}
                  onChange={(v) => updateField('자녀수', v)}
                  suffix="명"
                />
              </FormSection>

              {/* 보험료 */}
              <FormSection title="보험료">
                <NumberInput
                  label="국민연금 보험료"
                  value={formData.국민연금보험료}
                  onChange={(v) => updateField('국민연금보험료', v)}
                />
                <NumberInput
                  label="건강보험료"
                  value={formData.건강보험료}
                  onChange={(v) => updateField('건강보험료', v)}
                />
              </FormSection>

              {/* 의료비 */}
              <FormSection title="의료비">
                <NumberInput
                  label="의료비 지출액"
                  value={formData.의료비지출액}
                  onChange={(v) => updateField('의료비지출액', v)}
                />
                <NumberInput
                  label="노인/장애인 의료비"
                  value={formData.노인장애인의료비}
                  onChange={(v) => updateField('노인장애인의료비', v)}
                />
              </FormSection>

              {/* 기타 공제 */}
              <FormSection title="기타 공제">
                <NumberInput
                  label="기타 특별소득공제"
                  value={formData.기타특별소득공제}
                  onChange={(v) => updateField('기타특별소득공제', v)}
                />
              </FormSection>

              <button
                onClick={handleCalculate}
                className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors shadow-md"
              >
                계산하기
              </button>
            </div>
          </div>

          {/* 오른쪽: 결과 표시 */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6 border-b pb-3">
              📊 계산 결과
            </h2>

            {!showResult ? (
              <div className="text-center text-gray-500 py-20">
                왼쪽 정보를 입력하고 '계산하기' 버튼을 눌러주세요.
              </div>
            ) : (
              <div className="space-y-6">
                {/* Phase 2에서 실제 계산 결과 표시 */}
                <ResultSection title="소득">
                  <ResultRow label="총급여" value={formatNumber(formData.총급여)} />
                  <ResultRow
                    label="근로소득공제"
                    value="-원"
                    className="text-blue-600"
                  />
                  <ResultRow label="근로소득금액" value="-원" bold />
                </ResultSection>

                <ResultSection title="소득공제">
                  <ResultRow label="기본공제" value="-원" />
                  <ResultRow label="추가공제" value="-원" />
                  <ResultRow label="국민연금 등" value="-원" />
                  <ResultRow label="의료비공제" value="-원" />
                  <ResultRow label="기타공제" value="-원" />
                  <ResultRow
                    label="소득공제 합계"
                    value="-원"
                    bold
                    className="text-blue-600"
                  />
                </ResultSection>

                <ResultSection title="과세표준 및 산출세액">
                  <ResultRow label="과세표준" value="-원" bold />
                  <ResultRow
                    label="산출세액"
                    value="-원"
                    bold
                    className="text-red-600"
                  />
                </ResultSection>

                <ResultSection title="세액공제">
                  <ResultRow label="자녀세액공제" value="-원" />
                  <ResultRow label="근로소득세액공제" value="-원" />
                  <ResultRow
                    label="세액공제 합계"
                    value="-원"
                    bold
                    className="text-green-600"
                  />
                </ResultSection>

                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6 rounded-lg shadow-md">
                  <div className="text-sm opacity-90 mb-1">최종 결정세액</div>
                  <div className="text-3xl font-bold">계산 중...</div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 안내 문구 */}
        <footer className="mt-10 text-center text-sm text-gray-600">
          <p>※ 이 계산기는 2025년 개정 세법을 반영한 연말정산 시뮬레이션입니다.</p>
          <p>※ 실제 세액은 개인의 상황에 따라 달라질 수 있습니다.</p>
        </footer>
      </div>
    </div>
  );
}

// UI 컴포넌트들
function FormSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h3 className="text-lg font-semibold text-gray-700 mb-3">{title}</h3>
      <div className="space-y-3">{children}</div>
    </section>
  );
}

function NumberInput({
  label,
  value,
  onChange,
  placeholder,
  suffix,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
  placeholder?: string;
  suffix?: string;
}) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <div className="flex items-center">
        <input
          type="number"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          placeholder={placeholder}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        />
        {suffix && <span className="ml-2 text-sm text-gray-600">{suffix}</span>}
      </div>
    </div>
  );
}

function CheckboxInput({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <label className="flex items-center space-x-2 cursor-pointer">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
      />
      <span className="text-sm font-medium text-gray-700">{label}</span>
    </label>
  );
}

function ResultSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="border-b pb-4">
      <h3 className="text-lg font-semibold text-gray-700 mb-3">{title}</h3>
      <div className="space-y-2">{children}</div>
    </div>
  );
}

function ResultRow({
  label,
  value,
  bold = false,
  className = '',
}: {
  label: string;
  value: string;
  bold?: boolean;
  className?: string;
}) {
  return (
    <div className={`flex justify-between ${bold ? 'font-semibold' : ''} ${className}`}>
      <span className="text-gray-600">{label}</span>
      <span>{value}</span>
    </div>
  );
}
