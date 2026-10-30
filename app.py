import streamlit as st
import pandas as pd
from simulator_engine import FrancePolicyEngine

st.set_page_config(page_title="France 2030 Prescriptive Simulator", layout="wide")

st.title("🇫🇷 France 2030: Macroeconomic & Prescriptive Policy Engine")
st.markdown("""
*Solving France's structural bottlenecks: Deindustrialization, the debt crisis, smicardization, and social stability through data-driven policy levers.*
""")

# Sidebar Controls (Policy Levers)
st.sidebar.header("🛠️ Policy Intervention Levers")

# Key new slider addressing deindustrialization and GDP boost
industrial_reshoring = st.sidebar.slider("🏭 Industrial Reshoring & Local Manufacturing Boost", 0.0, 2.0, 1.0, 0.2, 
                                         help="Simulates bringing back factories and supply chains to boost domestic GDP and high-skill jobs.")

tax_cut_corp = st.sidebar.slider("Corporate & Production Tax Cut (%)", 0.0, 0.10, 0.03, 0.01)
labor_tax_shift = st.sidebar.slider("Middle-Class Payroll Tax Relief (Smicardization Fix)", 0.0, 2.0, 1.0, 0.2)
pension_age = st.sidebar.slider("Target Retirement Age", 62, 65, 63, 1)

# Run Simulation
engine = FrancePolicyEngine()
results = engine.simulate_reforms(industrial_reshoring, tax_cut_corp, labor_tax_shift, pension_age)

# Display Metrics Dashboard
st.subheader("📊 Prescriptive Simulation Results & Impact")
col1, col2, col3 = st.columns(3)

col1.metric("Projected GDP", f"€{results['Projected GDP (€B)']}B", f"{results['GDP Growth Rate (%)']}% Growth (Industrial Boost Active)")
col2.metric("Debt-to-GDP Ratio", f"{results['New Debt-to-GDP (%)']}%", "Fiscal Trajectory")
col3.metric("Social Strike Risk Score", f"{results['Social Strike Risk Score (0-100)']}/100", "Lower is Safer", delta_color="inverse")

col4, col5 = st.columns(2)
col4.metric("Adjusted Median Net Wage", f"€{results['Adjusted Median Wage (€)']}", "Combating Smicardization")
col5.metric("Pension System Health Index", f"{results['Pension System Sustainability Index']}/100", "Long-term Viability")

st.markdown("---")
st.info("💡 **Key Insight:** Increasing industrial reshoring expands the manufacturing base, creating high-value local employment that directly compounds GDP growth while alleviating middle-class wage compression.")
