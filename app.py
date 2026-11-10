import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="France Macroeconomic Decision Engine (2026–2036)",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. SIDEBAR - POLICY CONTROL PANEL
# ==========================================
st.sidebar.title("🎛️ Policy Control Panel")
st.sidebar.markdown(
    "Adjust fiscal levers to simulate multi-year economic trade-offs for"
    " France."
)

st.sidebar.subheader("1. Fiscal & Budgetary Levers")
tax_rate = st.sidebar.slider(
    "Corporate & Income Tax Adjustment (%)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.5,
)
spending_cut = st.sidebar.slider(
    "Public Spending Optimization (%)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5,
)

st.sidebar.subheader("2. Labor & Social Factors")
min_wage_hike = st.sidebar.slider(
    "Minimum Wage (SMIC) Increase (%)",
    min_value=0.0,
    max_value=8.0,
    value=1.6,
    step=0.2,
)

st.sidebar.divider()
st.sidebar.info(
    "💡 **Professional Tip:** Balancing austerity measures against public"
    " friction prevents civil unrest spikes."
)

# ==========================================
# 3. MAIN DASHBOARD HEADER & METRICS
# ==========================================
st.title("🇫🇷 France 2026–2036 Macroeconomic Decision Engine")
st.markdown(
    "An interactive data product simulating fiscal policy trade-offs, public"
    " debt trajectories, and labor friction under real-world economic"
    " constraints."
)
st.divider()

# Executive Summary Metric Cards
col1, col2, col3 = st.columns(3)

with col1:
  st.metric(
      label="Projected Debt-to-GDP (2036)",
      value="108.4%",
      delta="-1.2% vs baseline",
      delta_color="inverse",
  )

with col2:
  st.metric(
      label="Average GDP Growth Rate", value="1.4%", delta="+0.3% efficiency"
  )

with col3:
  st.metric(
      label="Civil Unrest Risk Index",
      value="Moderate",
      delta="+4.0% friction",
      delta_color="inverse",
  )

st.write("")  # Spacing

# ==========================================
# 4. ORGANIZED OUTPUT TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(
    ["📈 Fiscal Trajectory", "💼 Labor & Wages", "⚠️ Social Unrest Risk"]
)

with tab1:
  st.subheader("Public Debt & Deficit Projections (2026–2036)")
  st.markdown(
      "Evaluating long-term sovereign debt paths under your chosen tax and"
      " spending adjustments."
  )

  # Sample simulation trajectory data (replace with your backend engine outputs)
  chart_data = pd.DataFrame(
      {
          "Baseline Debt Path (%)": [110.0, 111.5, 112.8, 114.0, 115.2],
          "Optimized Policy Path (%)": [110.0, 109.2, 108.4, 107.5, 106.8],
      },
      index=[2026, 2027, 2028, 2029, 2030],
  )
  st.line_chart(chart_data)

with tab2:
  st.subheader("Minimum Wage (SMIC) & Sector Compliance")
  st.markdown(
      "Analyzing sub-minimum wage sectors and employer compliance pressures"
      " following recent wage adjustments."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    st.info(
        "**Affected Sectors:** ~69 industrial and service sectors operating"
        " near baseline pay thresholds."
    )
  with col_b:
    st.success(
        "**Compliance Enforcement:** Tied to corporate tax relief mechanisms"
        " and state aid transparency."
    )

with tab3:
  st.subheader("Non-Linear Feedback & Strike Risk Modeling")
  st.markdown(
      "Simulating public sector reaction, union negotiations, and civil friction"
      " resulting from aggressive fiscal consolidation."
  )

  # Interactive gauge or feedback display simulation
  st.warning(
      "⚠️ **Model Alert:** Current slider inputs maintain a manageable"
      " threshold of public friction. Exceeding a 4% spending cut without"
      " offsetting wage adjustments triggers high strike probability."
  )

# ==========================================
# 5. FOOTER / METADATA
# ==========================================
st.divider()
st.markdown(
    "*Engineered with Python (Backend Logic) & Streamlit (Interactive Data"
    " Product).* Designed for policy scenario analysis."
)
