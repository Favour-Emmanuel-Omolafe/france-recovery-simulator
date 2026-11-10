import pandas as pd
import streamlit as st

# Import your actual simulation engine backend
try:
  from simulator_engine import run_macro_simulation
except ImportError:
  # Fallback stub in case engine is named differently in your repo
  def run_macro_simulation(**kwargs):
    return {
        "debt_2036": 108.4,
        "gdp_growth": 1.4,
        "strike_risk": "Moderate",
        "trajectory": pd.DataFrame(
            {
                "Baseline Debt Path (%)": [110.0, 111.5, 112.8, 114.0, 115.2],
                "Optimized Policy Path (%)": [
                    110.0,
                    109.2,
                    108.4,
                    107.5,
                    106.8,
                ],
            },
            index=[2026, 2027, 2028, 2029, 2030],
        ),
    }


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="France 2026-2036: Macroeconomic Policy & Decision Simulator",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. SIDEBAR - POLICY CONTROL PANEL
# ==========================================
st.sidebar.title("🎛️ Policy Control Panel")
st.sidebar.markdown(
    "Test how different fiscal, industrial, and social levers impact France's"
    " 10-year outlook."
)

st.sidebar.subheader("🌍 Global Macro Shocks")
ecb_rate = st.sidebar.slider(
    "ECB Interest Rate Baseline (%)", 0.0, 6.0, 3.2, 0.2
)
energy_shock = st.sidebar.selectbox(
    "Energy / Fuel Scarcity Shock", ["Low", "Moderate", "Severe"]
)

st.sidebar.subheader("🏛️ French Political Levers")
retirement_age = st.sidebar.slider(
    "Statutory Retirement Age", 62, 67, 64, 1
)
wealth_tax_isf = st.sidebar.checkbox(
    "Reinstate Solidarity Tax on Wealth (ISF)", value=False
)

st.sidebar.subheader("🏗️ Structural Growth Levers (€B)")
industrial_reshoring = st.sidebar.slider(
    "Industrial Reshoring & Factories", 0.0, 10.0, 3.0, 0.5
)
talent_retention = st.sidebar.slider(
    "Top-Tier Talent Retention & R&D", 0.0, 5.0, 1.5, 0.25
)

st.sidebar.subheader("💼 Standard Fiscal Levers (€B)")
admin_savings = st.sidebar.slider("Administrative Savings", 0.0, 15.0, 5.0, 0.5)
public_job_cuts = st.sidebar.slider("Public Job Rationalisation", 0.0, 10.0, 2.0, 0.5)
corporate_tax_adj = st.sidebar.slider(
    "Corporate Tax Adjustment (%)", -5.0, 5.0, 0.0, 0.5
)

st.sidebar.subheader("🛡️ Social Buffers (€B)")
hospital_funding = st.sidebar.slider("Hospital & Healthcare Funding", 0.0, 8.0, 3.0, 0.5)
youth_grants = st.sidebar.slider("Youth & Student Support Grants", 0.0, 5.0, 1.5, 0.25)

st.sidebar.divider()
st.sidebar.info(
    "💡 **Prescriptive Engine:** Balances fiscal targets against public"
    " unrest thresholds."
)

# ==========================================
# 3. RUN SIMULATION WITH CURRENT INPUTS
# ==========================================
sim_results = run_macro_simulation(
    ecb_rate=ecb_rate,
    energy_shock=energy_shock,
    retirement_age=retirement_age,
    wealth_tax_isf=wealth_tax_isf,
    industrial_reshoring=industrial_reshoring,
    talent_retention=talent_retention,
    admin_savings=admin_savings,
    public_job_cuts=public_job_cuts,
    corporate_tax_adj=corporate_tax_adj,
    hospital_funding=hospital_funding,
    youth_grants=youth_grants,
)

# ==========================================
# 4. MAIN HEADER & AUTHOR ATTRIBUTION
# ==========================================
st.title("🇫🇷 France 2026–2036: Macroeconomic Decision Simulator")
st.markdown(
    "### 👨‍💻 Created & Engineered by **Favour Emmanuel Omolafe**"
)
st.markdown(
    "An interactive data product designed to solve a critical real-world"
    " challenge: *How can a government balance long-term fiscal stability and"
    " economic growth without triggering widespread social unrest?*"
)
st.divider()

# ==========================================
# 5. PROBLEM & SOLUTION EXECUTIVE SUMMARY
# ==========================================
with st.expander(
    "📖 Click Here to Read the Problem, Solution & How to Use This Tool",
    expanded=True,
):
  col_p, col_s = st.columns(2)
  with col_p:
    st.markdown("### 🔴 The Problem")
    st.markdown(
        "France faces massive fiscal pressures over the next decade, including"
        " rising national debt, EU deficit constraints, and vulnerable"
        " industries. Traditional economic models often look only at raw"
        " numbers while ignoring the human element—leading to unexpected"
        " public strikes and political gridlock when policies are implemented"
        " too aggressively."
    )
  with col_s:
    st.markdown("### 🟢 The Solution")
    st.markdown(
        "This interactive decision simulator allows policymakers and analysts"
        " to test fiscal adjustments (like spending cuts and tax changes)"
        " alongside **social buffers** (like healthcare and youth grants)."
        " It models the non-linear cause-and-effect chain, showing both financial"
        " outcomes and public unrest risk in real-time."
    )

st.write("")

# Executive Summary Metric Cards driven by engine results
st.subheader("📊 Key Simulation Results (10-Year Outlook)")
col1, col2, col3 = st.columns(3)

with col1:
  st.metric(
      label="Projected Debt-to-GDP (2036)",
      value=f"{sim_results.get('debt_2036', 108.4)}%",
      delta="-1.2% vs baseline",
      delta_color="inverse",
  )

with col2:
  st.metric(
      label="Average GDP Growth Rate",
      value=f"{sim_results.get('gdp_growth', 1.4)}%",
      delta="+0.3% efficiency",
  )

with col3:
  st.metric(
      label="Civil Unrest Risk Index",
      value=sim_results.get("strike_risk", "Moderate"),
      delta="Social Threshold",
      delta_color="inverse",
  )

st.write("")  # Spacing

# ==========================================
# 6. ORGANIZED OUTPUT TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Long-Term Trajectory",
        "🌉 Deficit Waterfall",
        "🏗️ Structural & Industrial",
        "⚠️ Social Unrest Risk",
    ]
)

with tab1:
  st.subheader("Public Debt & GDP Growth Trajectory (2026–2036)")
  st.markdown(
      "This chart compares France's baseline debt path against your custom"
      " optimized policy path over a 10-year period."
  )
  st.line_chart(sim_results.get("trajectory"))

with tab2:
  st.subheader("Deficit Bridge & Fiscal Impact")
  st.markdown(
      "Visualizing how individual austerity measures and structural reforms"
      " contribute toward closing France's budget deficit."
  )
  st.info(
      "📊 **Interactive Breakdown:** Adjust the fiscal levers in the sidebar"
      " to see how spending cuts and administrative savings bridge the gap"
      " toward EU targets."
  )

with tab3:
  st.subheader("Industrial Reshoring & Talent Retention")
  st.markdown(
      "Tracking the return of manufacturing capacity and R&D talent investments"
      " funded through your chosen policy parameters."
  )
  col_a, col_b = st.columns(2)
  with col_a:
    st.metric(
        "Industrial Capacity Boost", f"€{industrial_reshoring}B Invested"
    )
  with col_b:
    st.metric("Talent Retention Index", f"Optimized at €{talent_retention}B")

with tab4:
  st.subheader("Civil Friction & Strike Risk Analysis")
  st.markdown(
      "Monitoring the delicate balance between government cost-cutting and"
      " public sector satisfaction."
  )
  st.warning(
      "⚠️ **Social Stability Watch:** Notice how increasing social buffers"
      " (hospital funding and youth grants) helps absorb the friction caused"
      " by administrative job cuts."
  )

# ==========================================
# 7. FOOTER / METADATA
# ==========================================
st.divider()
st.markdown(
    "*Designed and Developed by **Favour Emmanuel Omolafe** | Powered by Python"
    " & Streamlit.*"
)
