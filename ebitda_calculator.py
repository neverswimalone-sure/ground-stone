#!/usr/bin/env python3
"""
EBITDA 및 기업가치(EV) 계산기
사용자로부터 재무 데이터를 입력받아 EBITDA와 기업가치를 계산합니다.
"""

def format_number(num):
    """숫자를 천 단위 구분 기호로 포맷팅"""
    return f"{num:,.0f}"

def get_positive_number(prompt):
    """양수 입력을 받는 함수"""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("❌ 0 이상의 값을 입력해주세요.")
                continue
            return value
        except ValueError:
            print("❌ 올바른 숫자를 입력해주세요.")

def calculate_ebitda(operating_profit, depreciation):
    """EBITDA 계산

    Args:
        operating_profit: 영업이익 (EBIT)
        depreciation: 감가상각비

    Returns:
        EBITDA 값
    """
    return operating_profit + depreciation

def calculate_enterprise_value(ebitda, multiple):
    """기업가치(EV) 계산

    Args:
        ebitda: EBITDA 값
        multiple: 멀티플 (배수)

    Returns:
        기업가치 (Enterprise Value)
    """
    return ebitda * multiple

def main():
    print("=" * 60)
    print("EBITDA 및 기업가치(EV) 계산기")
    print("=" * 60)
    print()

    # 사용자 입력
    revenue = get_positive_number("매출액을 입력하세요 (단위: 억원): ")
    operating_profit = get_positive_number("영업이익을 입력하세요 (단위: 억원): ")
    depreciation = get_positive_number("감가상각비를 입력하세요 (단위: 억원): ")

    # 멀티플 입력 (기본값: 8배)
    multiple_input = input("\n업종 평균 멀티플을 입력하세요 (기본값: 8배, Enter로 건너뛰기): ").strip()
    if multiple_input:
        try:
            multiple = float(multiple_input)
            if multiple <= 0:
                print("⚠️  0보다 큰 값을 입력해야 합니다. 기본값 8배를 사용합니다.")
                multiple = 8.0
        except ValueError:
            print("⚠️  올바르지 않은 입력입니다. 기본값 8배를 사용합니다.")
            multiple = 8.0
    else:
        multiple = 8.0

    # EBITDA 계산
    ebitda = calculate_ebitda(operating_profit, depreciation)

    # 기업가치 계산
    enterprise_value = calculate_enterprise_value(ebitda, multiple)

    # 결과 출력
    print("\n" + "=" * 60)
    print("📊 계산 결과")
    print("=" * 60)
    print(f"\n매출액:           {format_number(revenue)} 억원")
    print(f"영업이익 (EBIT):  {format_number(operating_profit)} 억원")
    print(f"감가상각비:       {format_number(depreciation)} 억원")
    print(f"\n{'─' * 60}")
    print(f"EBITDA:           {format_number(ebitda)} 억원")
    print(f"                  (영업이익 {format_number(operating_profit)} + 감가상각비 {format_number(depreciation)})")
    print(f"\n{'─' * 60}")
    print(f"적용 멀티플:      {multiple}배")
    print(f"기업가치 (EV):    {format_number(enterprise_value)} 억원")
    print(f"                  (EBITDA {format_number(ebitda)} × {multiple}배)")
    print("=" * 60)

    # 참고 지표 계산
    if revenue > 0:
        ebitda_margin = (ebitda / revenue) * 100
        print(f"\n📈 참고 지표")
        print(f"EBITDA 마진:      {ebitda_margin:.2f}%")
        print("=" * 60)

if __name__ == "__main__":
    main()
