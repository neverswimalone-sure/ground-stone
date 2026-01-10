import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="Golf Course M&A Valuation Dashboard",
    page_icon="⛳",
    layout="wide"
)

# 제목 및 설명
st.title("⛳ Golf Course M&A Valuation Dashboard")
st.markdown("**Investment Banking Advisory Tool** - 18홀 골프장 인수 실사 분석")
st.divider()

# 기본 가정
OPERATING_EXPENSE_RATIO = 0.45  # 45%
HOLES = 18

# 사이드바 - 주요 입력 변수
st.sidebar.header("📊 Valuation Parameters")

# 1. 객단가 슬라이더
price_per_customer = st.sidebar.slider(
    "1인당 객단가 (KRW)",
    min_value=90000,
    max_value=130000,
    value=110000,
    step=5000,
    format="%d"
)

# 2. 내장객 수 슬라이더
annual_visitors = st.sidebar.slider(
    "연간 내장객 수 (명)",
    min_value=120000,
    max_value=160000,
    value=140000,
    step=5000,
    format="%d"
)

# 3. EV/EBITDA 배수 슬라이더
ev_ebitda_multiple = st.sidebar.slider(
    "EV/EBITDA Multiple",
    min_value=5.0,
    max_value=12.0,
    value=8.0,
    step=0.5,
    format="%.1fx"
)

st.sidebar.divider()
st.sidebar.markdown(f"**고정 가정**")
st.sidebar.markdown(f"- 홀 수: {HOLES}홀")
st.sidebar.markdown(f"- Operating Expenses: {OPERATING_EXPENSE_RATIO*100:.0f}% of Revenue")

# 재무 계산 함수
def calculate_financials(visitors, price):
    revenue = visitors * price
    operating_expenses = revenue * OPERATING_EXPENSE_RATIO
    ebitda = revenue - operating_expenses
    return {
        'revenue': revenue / 100000000,  # 억원
        'opex': operating_expenses / 100000000,  # 억원
        'ebitda': ebitda / 100000000,  # 억원
        'ebitda_margin': (ebitda / revenue) * 100  # %
    }

# 현재 선택된 값으로 계산
financials = calculate_financials(annual_visitors, price_per_customer)
enterprise_value = financials['ebitda'] * ev_ebitda_multiple

# 메인 대시보드 - KPI 카드
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 매출 (Revenue)",
        value=f"{financials['revenue']:.1f}억원",
        delta=f"{price_per_customer/1000:.0f}k x {annual_visitors/1000:.0f}k명"
    )

with col2:
    st.metric(
        label="📉 Operating Expenses",
        value=f"{financials['opex']:.1f}억원",
        delta=f"{OPERATING_EXPENSE_RATIO*100:.0f}% of revenue"
    )

with col3:
    st.metric(
        label="📈 EBITDA",
        value=f"{financials['ebitda']:.1f}억원",
        delta=f"Margin: {financials['ebitda_margin']:.1f}%"
    )

with col4:
    st.metric(
        label="🏢 Enterprise Value (EV)",
        value=f"{enterprise_value:.1f}억원",
        delta=f"{ev_ebitda_multiple:.1f}x EBITDA"
    )

st.divider()

# 탭으로 다른 뷰 제공
tab1, tab2, tab3 = st.tabs(["📊 Sensitivity Analysis", "📈 Scenario Analysis", "📋 Deal Summary"])

with tab1:
    st.subheader("EBITDA Sensitivity Heatmap")

    # 민감도 분석 범위
    price_range = np.arange(90000, 135000, 5000)
    visitor_range = np.arange(120000, 165000, 5000)

    # EBITDA 테이블 생성
    ebitda_matrix = np.zeros((len(visitor_range), len(price_range)))

    for i, v in enumerate(visitor_range):
        for j, p in enumerate(price_range):
            fin = calculate_financials(v, p)
            ebitda_matrix[i, j] = fin['ebitda']

    # Plotly 히트맵
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=ebitda_matrix,
        x=[f'{p//1000}k' for p in price_range],
        y=[f'{v//1000}k' for v in visitor_range],
        colorscale='RdYlGn',
        text=ebitda_matrix,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        colorbar=dict(title="EBITDA<br>(억원)")
    ))

    fig_heatmap.update_layout(
        title="EBITDA Sensitivity Analysis (억원)",
        xaxis_title="Price per Customer (KRW)",
        yaxis_title="Annual Visitors",
        height=600,
        font=dict(size=12)
    )

    # 현재 선택된 값 강조
    current_price_idx = np.where(price_range == price_per_customer)[0]
    current_visitor_idx = np.where(visitor_range == annual_visitors)[0]

    if len(current_price_idx) > 0 and len(current_visitor_idx) > 0:
        fig_heatmap.add_trace(go.Scatter(
            x=[f'{price_per_customer//1000}k'],
            y=[f'{annual_visitors//1000}k'],
            mode='markers',
            marker=dict(size=20, color='blue', symbol='x', line=dict(width=2, color='white')),
            name='Current Selection',
            showlegend=True
        ))

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # EV 민감도 분석
    st.subheader("Enterprise Value (EV) Sensitivity Heatmap")

    ev_matrix = ebitda_matrix * ev_ebitda_multiple

    fig_ev = go.Figure(data=go.Heatmap(
        z=ev_matrix,
        x=[f'{p//1000}k' for p in price_range],
        y=[f'{v//1000}k' for v in visitor_range],
        colorscale='Viridis',
        text=ev_matrix,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        colorbar=dict(title="EV<br>(억원)")
    ))

    fig_ev.update_layout(
        title=f"Enterprise Value (EV) at {ev_ebitda_multiple:.1f}x EBITDA (억원)",
        xaxis_title="Price per Customer (KRW)",
        yaxis_title="Annual Visitors",
        height=600,
        font=dict(size=12)
    )

    if len(current_price_idx) > 0 and len(current_visitor_idx) > 0:
        fig_ev.add_trace(go.Scatter(
            x=[f'{price_per_customer//1000}k'],
            y=[f'{annual_visitors//1000}k'],
            mode='markers',
            marker=dict(size=20, color='cyan', symbol='x', line=dict(width=2, color='white')),
            name='Current Selection',
            showlegend=True
        ))

    st.plotly_chart(fig_ev, use_container_width=True)

with tab2:
    st.subheader("Scenario Analysis Comparison")

    # 3가지 시나리오 정의
    scenarios = {
        'Base Case': {'visitors': 140000, 'price': 110000},
        'Bull Case': {'visitors': 160000, 'price': 130000},
        'Bear Case': {'visitors': 120000, 'price': 90000},
        'Current': {'visitors': annual_visitors, 'price': price_per_customer}
    }

    scenario_results = []
    for scenario_name, params in scenarios.items():
        fin = calculate_financials(params['visitors'], params['price'])
        ev = fin['ebitda'] * ev_ebitda_multiple
        scenario_results.append({
            'Scenario': scenario_name,
            'Visitors': f"{params['visitors']:,}",
            'Price': f"₩{params['price']:,}",
            'Revenue (억원)': f"{fin['revenue']:.1f}",
            'EBITDA (억원)': f"{fin['ebitda']:.1f}",
            'EBITDA Margin': f"{fin['ebitda_margin']:.1f}%",
            'EV (억원)': f"{ev:.1f}"
        })

    scenario_df = pd.DataFrame(scenario_results)
    st.dataframe(scenario_df, use_container_width=True, hide_index=True)

    # 시나리오 비교 차트
    col1, col2 = st.columns(2)

    with col1:
        fig_scenario_ebitda = px.bar(
            scenario_df,
            x='Scenario',
            y=[float(x.replace(',', '')) for x in scenario_df['EBITDA (억원)']],
            title='EBITDA Comparison by Scenario',
            labels={'y': 'EBITDA (억원)'},
            color='Scenario',
            text_auto='.1f'
        )
        st.plotly_chart(fig_scenario_ebitda, use_container_width=True)

    with col2:
        fig_scenario_ev = px.bar(
            scenario_df,
            x='Scenario',
            y=[float(x.replace(',', '')) for x in scenario_df['EV (억원)']],
            title='Enterprise Value Comparison by Scenario',
            labels={'y': 'EV (억원)'},
            color='Scenario',
            text_auto='.1f'
        )
        st.plotly_chart(fig_scenario_ev, use_container_width=True)

with tab3:
    st.subheader("📋 M&A Deal Summary Report")

    st.markdown(f"""
    ### Deal Overview
    - **Target**: 18-Hole Golf Course
    - **Analysis Date**: 2026-01-10
    - **Valuation Method**: EBITDA Multiple Approach

    ---

    ### Operating Assumptions
    | Metric | Value |
    |--------|-------|
    | Annual Visitors | {annual_visitors:,} 명 |
    | Price per Customer | ₩{price_per_customer:,} |
    | Operating Expense Ratio | {OPERATING_EXPENSE_RATIO*100:.0f}% |

    ---

    ### Financial Performance (억원)
    | Item | Amount |
    |------|--------|
    | Revenue | {financials['revenue']:.1f} 억원 |
    | Operating Expenses | {financials['opex']:.1f} 억원 |
    | **EBITDA** | **{financials['ebitda']:.1f} 억원** |
    | EBITDA Margin | {financials['ebitda_margin']:.1f}% |

    ---

    ### Valuation
    | Item | Value |
    |------|-------|
    | EV/EBITDA Multiple | {ev_ebitda_multiple:.1f}x |
    | **Enterprise Value (EV)** | **{enterprise_value:.1f} 억원** |

    ---

    ### Key Investment Highlights
    1. **Stable Cash Flow**: EBITDA margin of {financials['ebitda_margin']:.1f}% indicates strong operational efficiency
    2. **Market Position**: Annual visitor volume of {annual_visitors:,} demonstrates solid market demand
    3. **Valuation Range**: Based on sensitivity analysis, EV ranges from {(ebitda_matrix.min() * ev_ebitda_multiple):.1f}억 to {(ebitda_matrix.max() * ev_ebitda_multiple):.1f}억

    ---

    ### Recommendation
    Based on the current parameters:
    - **EBITDA**: {financials['ebitda']:.1f}억원
    - **Implied EV**: {enterprise_value:.1f}억원 at {ev_ebitda_multiple:.1f}x multiple

    """)

    # 다운로드 버튼 (CSV)
    col1, col2 = st.columns(2)

    with col1:
        sensitivity_df = pd.DataFrame(
            ebitda_matrix,
            index=[f'{v:,}' for v in visitor_range],
            columns=[f'{p:,}' for p in price_range]
        )
        csv = sensitivity_df.to_csv()
        st.download_button(
            label="📥 Download EBITDA Sensitivity (CSV)",
            data=csv,
            file_name="golf_ebitda_sensitivity.csv",
            mime="text/csv"
        )

    with col2:
        ev_sensitivity_df = pd.DataFrame(
            ev_matrix,
            index=[f'{v:,}' for v in visitor_range],
            columns=[f'{p:,}' for p in price_range]
        )
        ev_csv = ev_sensitivity_df.to_csv()
        st.download_button(
            label="📥 Download EV Sensitivity (CSV)",
            data=ev_csv,
            file_name="golf_ev_sensitivity.csv",
            mime="text/csv"
        )

# Footer
st.divider()
st.caption("⚠️ This dashboard is for illustrative purposes only. Actual M&A valuations require comprehensive due diligence.")
