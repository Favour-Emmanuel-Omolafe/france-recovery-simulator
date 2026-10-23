import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="France 2030 Simulator", layout="wide")

# 1. The Comprehensive Simulation Engine (Now with Job & Tax Cuts)
def simulate_comprehensive_france(admin_savings_bn, pension_savings_bn, public_job_cuts_bn, corporate_tax_cut_bn, hospital_reinvest_bn, student_budget_bn, net_immigration_economic_impact, geopolitical_shock, use_article_49_3, union_pact, horizon=10):
    years = [2026 + i for i in range(horizon + 1)]
    debt, deficit = np.zeros(horizon + 1), np.zeros(horizon + 1)
    unrest, spread, gdp_growth = np.zeros(horizon + 1), np.zeros(horizon + 1), np.zeros(horizon + 1)

    # 2026 Baseline
    debt[0], deficit[0], unrest[0], spread[0], gdp_growth[0] = 119.0, 5.0, 42.0, 80.0, 0.7
    nom_gdp = 3100.0

    for t in range(horizon):
        shock_penalty = 12.0 if (geopolitical_shock and t == 2) else 0.0
        demographic_growth_modifier = net_immigration_economic_impact * 0.15
        
        # Unrest Calculation (Job cuts trigger massive protests; Tax cuts annoy unions regarding inequality)
        grievance = 42.0 + (admin_savings_bn * 0.25) + (pension_savings_bn * 1.5) + (public_job_cuts_bn * 2.5) + (corporate_tax_cut_bn * 0.5)
        if use_article_49_3:
            grievance += 22.0
        grievance -= (hospital_reinvest_bn * 1.8)
        grievance -= (student_budget_bn * 1.2)
        if union_pact:
            grievance -= 18.0
            
        unrest[t+1] = np.clip(0.60 * unrest[t] + 0.40 * grievance, 0, 100)
        strike_drag = 0.65 if unrest[t+1] >= 75.0 else 0.0
        
        # MACROECONOMIC EFFECT: Job cuts drag consumption down; Tax cuts boost business investment
        job_cut_drag = public_job_cuts_bn * 0.02
        tax_cut_boost = corporate_tax_cut_bn * 0.04
        
        gdp_growth[t+1] = 0.7 + demographic_growth_modifier + tax_cut_boost - job_cut_drag - strike_drag
        
        # Fiscal Calculation (Net balance of all cuts vs all spending)
        net_fiscal_effort = admin_savings_bn + pension_savings_bn + public_job_cuts_bn - hospital_reinvest_bn - student_budget_bn - corporate_tax_cut_bn - shock_penalty
        fiscal_pct_gdp = (net_fiscal_effort / nom_gdp) * 100.0
        growth_dividend = (gdp_growth[t+1] - 0.7) * 0.4
        
        deficit[t+1] = np.clip(deficit[t] - (fiscal_pct_gdp - 0.25) - growth_dividend, 1.5, 9.0)
        
        spread_fisc = 9.5 * max(0.0, deficit[t+1] - 3.0)
        spread[t+1] = 35.0 + spread_fisc + (0.40 * unrest[t+1]) + (15.0 if geopolitical_shock else 0.0)
        
        r_eff = (2.5 + (spread[t+1] / 100.0)) / 100.0
        g_nom = (gdp_growth[t+1] + 2.0) / 100.0
        debt[t+1] = debt[t] * ((1.0 + r_eff) / (1.0 + g_nom)) + deficit[t+1] - (0.35 * gdp_growth[t+1])
        
    return pd.DataFrame({'Year': years, 'Debt_GDP': debt, 'Deficit_GDP': deficit, 'Unrest_Index': unrest, 'OAT_Spread': spread, 'GDP_Growth': gdp_growth})

# 2. UI & Sidebar Controls
st.title("🇫🇷 France 2030+: Macro-Fiscal & Democratic Recovery Simulator")
st.markdown("Stress-test the French economy by balancing austerity, tax policy, and social stability.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Favour Emmanuel Omolafe**")
st.sidebar.markdown("---")

st.sidebar.header("Economic & Fiscal Levers")
admin_cuts = st.sidebar.slider("Administrative Savings (€B)", 0.0, 30.0, 15.0, step=1.0)
public_job_cuts = st.sidebar.slider("Public Sector Job Cuts (€B) ⚠️", 0.0, 15.0, 0.0, step=1.0, help="Saves money, but drags down GDP consumption and massively triggers union strikes.")
pension_cuts = st.sidebar.slider("Pension Reform Savings (€B) ⚠️", 0.0, 20.0, 0.0, step=1.0)
corporate_tax_cuts = st.sidebar.slider("Corporate Tax Cuts (€B)", 0.0, 20.0, 0.0, step=1.0, help="Increases the deficit initially, but boosts GDP growth through business investment.")

st.sidebar.header("Social & Demographic Levers")
hospital_inv = st.sidebar.slider("Hospital Reinvestment (€B)", 0.0, 10.0, 3.0, step=0.5)
student_budget = st.sidebar.slider("Student & Youth Grants (€B)", 0.0, 10.0, 2.0, step=0.5)
immigration = st.sidebar.slider("Net Labor Integration Impact", -5.0, 5.0, 1.0, step=0.5)

st.sidebar.header("Political Levers")
use_49_3 = st.sidebar.checkbox("Bypass Parliament (Article 49.3)", value=False)
union_pact = st.sidebar.checkbox("Sign Tripartite Union Pact", value=True)
geo_shock = st.sidebar.checkbox("Trigger Geopolitical Escalation Shock", value=False)

# 3. Run Simulation & Display Results
df_results = simulate_comprehensive_france(admin_cuts, pension_cuts, public_job_cuts, corporate_tax_cuts, hospital_inv, student_budget, immigration, geo_shock, use_49_3, union_pact)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("2036 Debt-to-GDP", f"{df_results['Debt_GDP'].iloc[-1]:.1f}%")
col2.metric("2036 Deficit", f"{df_results['Deficit_GDP'].iloc[-1]:.1f}%")
col3.metric("2036 GDP Growth", f"{df_results['GDP_Growth'].iloc[-1]:.1f}%")

unrest_score = df_results['Unrest_Index'].iloc[-1]
col4.metric("Strike Risk Index", f"{unrest_score:.1f}", "CRITICAL" if unrest_score >= 75 else "Stable", delta_color="inverse")
col5.metric("10-Yr Spread", f"{df_results['OAT_Spread'].iloc[-1]:.0f} bps")

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
plt.style.use('seaborn-v0_8-whitegrid')

axes[0,0].plot(df_results['Year'], df_results['Debt_GDP'], color='#002395', lw=3)
axes[0,0].set_title("Gross Public Debt (% of GDP)", fontweight='bold')
axes[0,0].axhline(100.0, color='gray', linestyle='--')

axes[0,1].plot(df_results['Year'], df_results['Unrest_Index'], color='#ED2939', lw=3)
axes[0,1].set_title("Social Unrest Index (Strike > 75)", fontweight='bold')
axes[0,1].axhline(75.0, color='darkred', linestyle=':')

axes[1,0].plot(df_results['Year'], df_results['Deficit_GDP'], color='purple', lw=3)
axes[1,0].set_title("Budget Deficit (% of GDP)", fontweight='bold')
axes[1,0].axhline(3.0, color='red', linestyle='--', label='EU 3% Limit')

axes[1,1].plot(df_results['Year'], df_results['GDP_Growth'], color='green', lw=3)
axes[1,1].set_title("Annual GDP Growth (%)", fontweight='bold')

plt.tight_layout()
st.pyplot(fig)
