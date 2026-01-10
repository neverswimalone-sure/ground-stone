import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Linux 환경)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 기본 가정
OPERATING_EXPENSE_RATIO = 0.45  # 45%

# 민감도 분석 범위 설정
# 객단가: 9만원 ~ 13만원 (5천원 단위)
price_per_customer = np.arange(90000, 135000, 5000)  # 90k, 95k, 100k, ..., 130k

# 내장객 수: 12만명 ~ 16만명 (5천명 단위)
visitors = np.arange(120000, 165000, 5000)  # 120k, 125k, 130k, ..., 160k

# EBITDA 계산 함수
def calculate_ebitda(visitors_count, price):
    revenue = visitors_count * price
    operating_expenses = revenue * OPERATING_EXPENSE_RATIO
    ebitda = revenue - operating_expenses
    return ebitda / 100000000  # 억원 단위로 변환

# 민감도 분석 테이블 생성
ebitda_table = pd.DataFrame(
    index=[f'{v//1000}k' for v in visitors],  # 천명 단위로 표시
    columns=[f'{p//1000}k' for p in price_per_customer]  # 천원 단위로 표시
)

# EBITDA 값 계산
for i, v in enumerate(visitors):
    for j, p in enumerate(price_per_customer):
        ebitda_table.iloc[i, j] = calculate_ebitda(v, p)

# 숫자형으로 변환
ebitda_table = ebitda_table.astype(float)

# 히트맵 생성
plt.figure(figsize=(16, 10))
sns.heatmap(
    ebitda_table,
    annot=True,  # 숫자 표시
    fmt='.1f',   # 소수점 1자리
    cmap='RdYlGn',  # 빨강-노랑-초록 색상 (낮음-중간-높음)
    cbar_kws={'label': 'EBITDA (billion KRW)'},
    linewidths=0.3,
    linecolor='gray',
    annot_kws={'size': 8}
)

plt.title('Golf Course M&A - EBITDA Sensitivity Analysis (Detailed)\n(EBITDA in billion KRW)',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Price per Customer (KRW)', fontsize=12, fontweight='bold')
plt.ylabel('Annual Visitors', fontsize=12, fontweight='bold')

# 축 라벨 회전
plt.xticks(rotation=0)
plt.yticks(rotation=0)

# 레이아웃 조정
plt.tight_layout()

# 이미지 저장 (고해상도)
plt.savefig('golf_ebitda_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Sensitivity analysis heatmap saved as 'golf_ebitda_sensitivity_analysis.png'")

# 기본 케이스 EBITDA 출력
base_ebitda = calculate_ebitda(140000, 110000)
print(f"\n=== Base Case EBITDA ===")
print(f"Visitors: 140,000")
print(f"Price per customer: 110,000 KRW")
print(f"Revenue: {140000 * 110000 / 100000000:.1f} billion KRW")
print(f"Operating Expenses (45%): {140000 * 110000 * 0.45 / 100000000:.1f} billion KRW")
print(f"EBITDA: {base_ebitda:.1f} billion KRW")

# 데이터 테이블도 출력
print(f"\n=== EBITDA Sensitivity Table (billion KRW) ===")
print(ebitda_table.to_string())

plt.close()
