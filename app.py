import streamlit as st
import pandas as pd
from simulator_engine import FrancePolicyEngine

st.set_page_config(page_title="France 2030 Prescriptive Simulator", layout="wide")

st.title("🇫🇷 France 2030: Macroeconomic & Prescriptive Policy Engine")
st.markdown("""
*Moving beyond passive forecasting to solve structural bottlenecks: Debt crisis, smicardization, brain drain, and social strike risks.*
""")

# Sidebar Controls (Policy Levers)
st.sidebar.header("🛠️ Policy Intervention Levers")
tax_cut_corp = st.sidebar.slider("Corporate & Production Tax Cut (%)", 0.0, 0.10, 0.03, 0.01)
rd_subsidy = st.sidebar.slider("R&D & Talent Retention Subsidy Level", 0.0, 2.0, 1.0, 0.2)
labor_tax_shift = st.sidebar.slider("Middle-Class Payroll Tax Relief", 0.0, 2.0, 1.0, 0.2)
pension_age = st.sidebar.slider("Target Retirement Age", 62, 65, 63, 1)

# Run Simulation
engine = FrancePolicyEngine()
results = engine.simulate_reforms(tax_cut_corp, rd_subsidy, labor_tax_shift, pension_age)

# Display Metrics Dashboard
st.subheader("📊 Prescriptive Simulation Results")
col1, col2, col3 = st.columns(3)

col1.metric("Projected GDP", f"€{results['Projected GDP (€B)']}B", f"{results['GDP Growth Rate (%)']}% Growth")
col2.metric("Debt-to-GDP Ratio", f"{results['New Debt-to-GDP (%)']}%", "-2.1% vs Baseline")
col3.metric("Social Strike Risk Score", f"{results['Social Strike Risk Score (0-100)']}/100", "Lower is Safer", delta_color="inverse")

col4, col5 = st.columns(2)
col4.metric("Adjusted Median Net Wage", f"€{results['Adjusted Median Wage (€)']}", "Combating Smicardization")
col5.metric("Pension System Health Index", f"{results['Pension System Sustainability Index']}/100", "Long-term Viability")

st.markdown("---")
st.info("💡 **Analyst Note:** Adjust the sidebar levers to simulate how targeted tax shifting and R&D credits optimize economic recovery while mitigating social unrest.")
