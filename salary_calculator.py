#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한국 연봉 기반 월 실수령액 계산기
2026년 기준 4대 보험 및 세금 계산
"""


def calculate_national_pension(monthly_salary):
    """국민연금 계산 (4.5%)"""
    # 상한액: 590만원, 하한액: 37만원
    base = min(max(monthly_salary, 370000), 5900000)
    return int(base * 0.045)


def calculate_health_insurance(monthly_salary):
    """건강보험 계산 (3.545%)"""
    return int(monthly_salary * 0.03545)


def calculate_long_term_care(health_insurance):
    """장기요양보험 계산 (건강보험의 12.95%)"""
    return int(health_insurance * 0.1295)


def calculate_employment_insurance(monthly_salary):
    """고용보험 계산 (0.9%)"""
    return int(monthly_salary * 0.009)


def calculate_income_tax(monthly_salary, dependents=1):
    """
    소득세 계산 (간이세액표 기준)
    dependents: 부양가족 수 (본인 포함)
    """
    # 2026년 간이세액표 (단순화된 버전)
    # 실제로는 더 복잡하지만, 대략적인 계산을 위한 누진세율 적용

    annual_taxable = monthly_salary * 12

    # 기본공제 적용 (1인당 150만원)
    deduction = 1500000 * dependents
    taxable = max(0, annual_taxable - deduction)

    # 누진세율 구간별 계산
    tax = 0
    if taxable <= 14000000:
        tax = taxable * 0.06
    elif taxable <= 50000000:
        tax = 14000000 * 0.06 + (taxable - 14000000) * 0.15
    elif taxable <= 88000000:
        tax = 14000000 * 0.06 + 36000000 * 0.15 + (taxable - 50000000) * 0.24
    elif taxable <= 150000000:
        tax = 14000000 * 0.06 + 36000000 * 0.15 + 38000000 * 0.24 + (taxable - 88000000) * 0.35
    elif taxable <= 300000000:
        tax = 14000000 * 0.06 + 36000000 * 0.15 + 38000000 * 0.24 + 62000000 * 0.35 + (taxable - 150000000) * 0.38
    elif taxable <= 500000000:
        tax = 14000000 * 0.06 + 36000000 * 0.15 + 38000000 * 0.24 + 62000000 * 0.35 + 150000000 * 0.38 + (taxable - 300000000) * 0.40
    else:
        tax = 14000000 * 0.06 + 36000000 * 0.15 + 38000000 * 0.24 + 62000000 * 0.35 + 150000000 * 0.38 + 200000000 * 0.40 + (taxable - 500000000) * 0.45

    monthly_tax = int(tax / 12)
    return monthly_tax


def calculate_local_income_tax(income_tax):
    """지방소득세 계산 (소득세의 10%)"""
    return int(income_tax * 0.1)


def calculate_take_home_pay(annual_salary, dependents=1):
    """
    연봉을 입력받아 월 실수령액을 계산

    Args:
        annual_salary: 연봉 (원)
        dependents: 부양가족 수 (본인 포함, 기본값 1)

    Returns:
        dict: 상세 계산 내역
    """
    monthly_salary = annual_salary / 12

    # 4대 보험 계산
    national_pension = calculate_national_pension(monthly_salary)
    health_insurance = calculate_health_insurance(monthly_salary)
    long_term_care = calculate_long_term_care(health_insurance)
    employment_insurance = calculate_employment_insurance(monthly_salary)

    # 세금 계산
    income_tax = calculate_income_tax(monthly_salary, dependents)
    local_income_tax = calculate_local_income_tax(income_tax)

    # 총 공제액
    total_deduction = (
        national_pension +
        health_insurance +
        long_term_care +
        employment_insurance +
        income_tax +
        local_income_tax
    )

    # 실수령액
    take_home = int(monthly_salary - total_deduction)

    return {
        '연봉': int(annual_salary),
        '월 급여': int(monthly_salary),
        '국민연금': national_pension,
        '건강보험': health_insurance,
        '장기요양보험': long_term_care,
        '고용보험': employment_insurance,
        '소득세': income_tax,
        '지방소득세': local_income_tax,
        '총 공제액': total_deduction,
        '월 실수령액': take_home
    }


def print_result(result):
    """계산 결과를 보기 좋게 출력"""
    print("\n" + "="*50)
    print("💰 월 실수령액 계산 결과")
    print("="*50)
    print(f"\n📊 기본 정보")
    print(f"  • 연봉: {result['연봉']:,}원")
    print(f"  • 월 급여: {result['월 급여']:,}원")

    print(f"\n🏥 4대 보험")
    print(f"  • 국민연금 (4.5%): {result['국민연금']:,}원")
    print(f"  • 건강보험 (3.545%): {result['건강보험']:,}원")
    print(f"  • 장기요양보험 (12.95%): {result['장기요양보험']:,}원")
    print(f"  • 고용보험 (0.9%): {result['고용보험']:,}원")

    print(f"\n💸 세금")
    print(f"  • 소득세: {result['소득세']:,}원")
    print(f"  • 지방소득세: {result['지방소득세']:,}원")

    print(f"\n📉 공제 합계")
    print(f"  • 총 공제액: {result['총 공제액']:,}원")

    print(f"\n✅ 최종 결과")
    print(f"  • 월 실수령액: {result['월 실수령액']:,}원")
    print("="*50 + "\n")


def main():
    """메인 함수"""
    print("\n🧮 한국 연봉 실수령액 계산기")
    print("="*50)

    try:
        # 연봉 입력
        annual_salary = float(input("\n연봉을 입력하세요 (원): ").replace(",", ""))

        # 부양가족 수 입력 (선택사항)
        dependents_input = input("부양가족 수를 입력하세요 (본인 포함, 기본값 1): ").strip()
        dependents = int(dependents_input) if dependents_input else 1

        # 계산 실행
        result = calculate_take_home_pay(annual_salary, dependents)

        # 결과 출력
        print_result(result)

    except ValueError:
        print("\n❌ 오류: 올바른 숫자를 입력해주세요.")
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
