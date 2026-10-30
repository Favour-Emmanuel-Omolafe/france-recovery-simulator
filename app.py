
from simulator_engine import FrancePolicyEngine

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import itertools

st.set_page_config(page_title="France 2030 Comprehensive Crisis & Solution Simulator", layout="wide")

# 1. The Core Engine (With Industrial Over-Capacity & Environmental/Economic Penalties)
def simulate_economy(admin_cut, retirement_age, wealth_tax, job_cut, tax_cut, hosp_inv, youth_grant, tech_inv, industrial_reshoring, medical_sovereignty, talent_retention, fuel_scarcity_lvl, war_shock, ecb_rate, horizon=10):
    years = [2026 + i for i in range(horizon + 1)]
    debt, deficit, unrest, gdp = np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1)
    
    debt[0], deficit[0], unrest[0], gdp[0] = 120.0, 5.4, 55.0, 0.4 
    nom_gdp = 3100.0

    for t in range(horizon):
        demographic_multiplier = 1.0 + (t * 0.03) 
        base_pension_savings = (retirement_age - 62) * 4.5
        pension_savings = base_pension_savings * demographic_multiplier if retirement_age > 62 else base_pension_savings
        
        wealth_tax_rev = 4.0 if wealth_tax else 0.0    
        
        grievance = 55.0 + (admin_cut * 0.3) + ((retirement_age - 62) * 12.0) + (job_cut * 3.5) + (tax_cut * 0.6)
        grievance += (fuel_scarcity_lvl * 4.0) 
        
        # REALITY CHECK: Pushing industrial reshoring past €6B strains the energy grid and sparks environmental backlash
        industrial_penalty_unrest = max(0, (industrial_reshoring - 6.0) * 3.0) if industrial_reshoring > 6.0 else 0.0
        
        grievance -= (hosp_inv * 2.0) + (youth_grant * 1.5) + (tech_inv * 0.5) + (min(industrial_reshoring, 6.0) * 1.0) + (medical_sovereignty * 0.8) + (talent_retention * 1.2)
        grievance += industrial_penalty_unrest
        
        if wealth_tax: grievance -= 5.0 
        
        unrest[t+1] = np.clip(0.6 * unrest[t] + 0.4 * grievance, 0, 100)
        strike_drag = 0.8 if unrest[t+1] >= 75.0 else 0.0
        
        war_drag = 0.4 if war_shock else 0.0
        fuel_drag = fuel_scarcity_lvl * 0.15
        wealth_tax_drag = 0.05 if wealth_tax else 0.0
        
        # DIMINISHING RETURNS / CARBON PENALTY MODEL:
        # Up to €6B = Clean industrial growth. Past €6B = Grid strain, carbon fines, and diminishing returns.
        if industrial_reshoring <= 6.0:
            industrial_gdp_boost = industrial_reshoring * 0.05
        else:
            industrial_gdp_boost = (6.0 * 0.05) - ((industrial_reshoring - 6.0) * 0.04)
            
        structural_gdp_boost = industrial_gdp_boost + (medical_sovereignty * 0.04) + (talent_retention * 0.06)
        
        gdp[t+1] = 0.4 + (tax_cut * 0.05) + (tech_inv * 0.08) + structural_gdp_boost - (job_cut * 0.05) - fuel_drag - war_drag - strike_drag - wealth_tax_drag
        
        real_job_savings = job_cut * 0.5 
        net_effort = admin_cut + pension_savings + wealth_tax_rev + real_job_savings - hosp_inv - youth_grant - tax_cut - tech_inv - industrial_reshoring - medical_sovereignty - talent_retention
        
        fiscal_pct = (net_effort / nom_gdp) * 100.0
        growth_div = (gdp[t+1] - 0.4) * 0.4
        deficit[t+1] = np.clip(deficit[t] - fiscal_pct - growth_div, 1.0, 15.0)
        
        war_premium = 20.0 if war_shock else 0.0
        risk_spread = (10.0 * max(0, deficit[t+1] - 3.0)) + (0.5 * unrest[t+1]) + war_premium
        
        r_eff = (ecb_rate + (risk_spread / 100.0)) / 100.0
        g_nom = (gdp[t+1] + 2.0) / 100.0 
        
        interest_burden = debt[t] * r_eff
        debt_reduction_from_growth = debt[t] * g_nom
        debt[t+1] = debt[t] + deficit[t+1] + interest_burden - debt_reduction_from_growth
        
    return pd.DataFrame({'Year': years, 'Debt_GDP': debt, 'Deficit_GDP': deficit, 'Unrest_Index': unrest, 'GDP_Growth': gdp})

# 2. The Auto-Solver 
def find_optimal_solution(current_fuel, current_war, current_ecb):
    best_combo = None
    lowest_unrest = 100
    
    admin = range(0, 6, 1)  
    ret_age = range(60, 68, 1) 
    job = range(0, 11, 2)
    tax = range(0, 11, 2)
    wealth_tx_opts = [True, False]
    
    for a, r, j, t, w in itertools.product(admin, ret_age, job, tax, wealth_tx_opts):
        h_inv, y_grant, tech_inv, ind_resh, med_sov, tal_ret = 3.0, 2.0, 3.0, 3.0, 2.0, 2.0
        df_sim = simulate_economy(a, r, w, j, t, h_inv, y_grant, tech_inv, ind_resh, med_sov, tal_ret, current_fuel, current_war, current_ecb)
        d_def, d_unrest = df_sim['Deficit_GDP'].iloc[-1], df_sim['Unrest_Index'].iloc[-1]
        
        if d_def <= 3.0 and d_unrest < 75.0:
            if d_unrest < lowest_unrest:
                lowest_unrest = d_unrest
                best_combo = (a, r, w, j, t, h_inv, y_grant, tech_inv, ind_resh, med_sov, tal_ret, d_def, d_unrest)
                
    return best_combo

# 3. Sidebar UI
st.sidebar.markdown("### 🇫🇷 France 2030 Comprehensive Optimizer\n**Built by Favour Emmanuel Omolafe**\n---")

st.sidebar.header("Global Macro Shocks")
ecb_rate = st.sidebar.slider("🏦 ECB Base Interest Rate (%)", 0.0, 5.0, st.session_state.get('ecb', 2.5), step=0.25)
fuel_shock = st.sidebar.slider("🌍 Fuel Scarcity & Energy Shock (0-5)", 0.0, 5.0, st.session_state.get('fuel', 0.0), step=1.0)
war_toggle = st.sidebar.checkbox("🌍 Global Geopolitical Conflict", value=st.session_state.get('war', False))

if st.sidebar.button("🤖 Auto-Solve for 3% Deficit (AI Optimizer)"):
    with st.spinner("Calculating optimal macroeconomic solutions..."):
        optimal = find_optimal_solution(fuel_shock, war_toggle, ecb_rate)
        if optimal:
            st.sidebar.success("Optimal Solution Found!")
            st.session_state['admin'] = float(optimal[0])
            st.session_state['ret_age'] = int(optimal[1])
            st.session_state['wealth_tax'] = optimal[2]
            st.session_state['job'] = float(optimal[3])
            st.session_state['tax'] = float(optimal[4])
        else:
            st.sidebar.error("CRITICAL: Global conditions too severe.")

st.sidebar.header("French Political Levers")
retire_age = st.sidebar.slider("Statutory Retirement Age", 60, 67, st.session_state.get('ret_age', 64), step=1)
wealth_tax = st.sidebar.checkbox("Reinstate Wealth Tax (ISF)", value=st.session_state.get('wealth_tax', False))

st.sidebar.header("Structural Growth Levers (€B)")
industrial_reshoring = st.sidebar.slider("🏭 Industrial Reshoring & Factories (€B)", 0.0, 10.0, 3.0, step=1.0, help="Optimal up to €6B. Pushing past €6B causes energy grid strain, carbon fines, and citizen friction.")
medical_sovereignty = st.sidebar.slider("🏥 Medical & Pharma Production (€B)", 0.0, 10.0, 2.0, step=1.0, help="Produces critical medicines locally to secure supply chains.")
talent_retention = st.sidebar.slider("🧠 Top-Tier Talent Retention & R&D (€B)", 0.0, 10.0, 2.0, step=1.0, help="Combats brain drain by retaining top scientists and engineers.")

st.sidebar.header("Standard Fiscal Levers (€B)")
tech_invest = st.sidebar.slider("General Tech & Digital Investment", 0.0, 10.0, 3.0, step=1.0)
admin_cuts = st.sidebar.slider("Admin Savings", 0.0, 5.0, st.session_state.get('admin', 2.0), step=1.0)
public_job_cuts = st.sidebar.slider("Job Cuts", 0.0, 15.0, st.session_state.get('job', 0.0), step=1.0)
corporate_tax_cuts = st.sidebar.slider("Tax Cuts", 0.0, 20.0, st.session_state.get('tax', 0.0), step=1.0)

st.sidebar.header("Social Buffers (€B)")
hospital_inv = st.sidebar.slider("Hospital Invest", 0.0, 10.0, 3.0, step=0.5)
student_budget = st.sidebar.slider("Youth Grants", 0.0, 10.0, 2.0, step=0.5)

# Run Simulation
df_results = simulate_economy(admin_cuts, retire_age, wealth_tax, public_job_cuts, corporate_tax_cuts, hospital_inv, student_budget, tech_invest, industrial_reshoring, medical_sovereignty, talent_retention, fuel_shock, war_toggle, ecb_rate)
final_debt, final_def, final_unrest, final_gdp = df_results.iloc[-1][['Debt_GDP', 'Deficit_GDP', 'Unrest_Index', 'GDP_Growth']]

# Main UI
st.title("🇫🇷 France 2026-2036: Comprehensive Crisis & Solution Optimizer")

if final_def <= 3.0 and final_unrest < 75:
    st.success(f"🏆 MACROECONOMIC TRILEMMA SOLVED: Deficit stabilized at {final_def:.1f}% with balanced industrial growth.")
elif final_unrest >= 75:
    st.error(f"🔥 GENERAL STRIKE: Strike Index hit {final_unrest:.1f}. Over-industrialization or severe austerity caused social unrest.")
elif final_def > 3.0:
    st.warning(f"📉 DEBT SPIRAL: Deficit is {final_def:.1f}%. Markets are reacting to fiscal imbalance.")

tab1, tab2 = st.tabs(["📊 Live Simulator", "🧠 Model Methodology"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("2036 Debt-to-GDP", f"{final_debt:.1f}%")
    col2.metric("2036 Deficit", f"{final_def:.1f}%", "EU Compliant" if final_def <= 3.0 else "Violation", delta_color="inverse")
    col3.metric("Strike Risk Index", f"{final_unrest:.1f}", "Stable" if final_unrest < 75 else "High Risk", delta_color="inverse")
    col4.metric("2036 GDP Growth", f"{final_gdp:.1f}%", "Balanced Growth")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        nom_gdp = 3100.0
        avg_pens_sav = ((retire_age - 62) * 4.5) * 1.15 
        wealth_rev = 4.0 if wealth_tax else 0.0
        real_job = public_job_cuts * 0.5
        
        imp_admin = -(admin_cuts / nom_gdp) * 100
        imp_pens = -(avg_pens_sav / nom_gdp) * 100
        imp_wealth = -(wealth_rev / nom_gdp) * 100
        imp_job = -(real_job / nom_gdp) * 100
        imp_tax = (corporate_tax_cuts / nom_gdp) * 100
        imp_spend = ((hospital_inv + student_budget + tech_invest + industrial_reshoring + medical_sovereignty + talent_retention) / nom_gdp) * 100
        dynamic_effect = final_def - (5.4 + imp_admin + imp_pens + imp_wealth + imp_job + imp_tax + imp_spend)

        fig1 = go.Figure(go.Waterfall(
            name = "Deficit Bridge", orientation = "v",
            measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
            x = ["2026 Baseline", "Austerity (Admin/Jobs)", "Pension Reform", "Wealth Tax", "New Spending/Cuts", "ECB & Growth Dynamics", "2036 Final"],
            textposition = "outside",
            y = [5.4, imp_admin+imp_job, imp_pens, imp_wealth, imp_tax+imp_spend, dynamic_effect, final_def],
            decreasing = {"marker":{"color":"#29b09d"}}, 
            increasing = {"marker":{"color":"#ff4b4b"}}, 
            totals = {"marker":{"color":"#0068c9"}}
        ))
        fig1.update_layout(title="Deficit Waterfall Bridge (% of GDP)", showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig1.add_hline(y=3.0, line_dash="dot")
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.line(df_results, x='Year', y='Debt_GDP', title='Gross Public Debt (% of GDP)', markers=True, color_discrete_sequence=['#0068c9'])
        st.plotly_chart(fig2, use_container_width=True)

    with col_chart2:
        fig3 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_unrest,
            title = {'text': "Strike Risk Speedometer"},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "rgba(0,0,0,0)"}, 
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "#29b09d"},
                    {'range': [50, 75], 'color': "#ffaa00"},
                    {'range': [75, 100], 'color': "#ff4b4b"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 6},
                    'thickness': 0.8,
                    'value': final_unrest
                }
            }
        ))
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.line(df_results, x='Year', y='GDP_Growth', title='Annual GDP Growth (%)', markers=True, color_discrete_sequence=['#0068c9'])
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.header("How the Comprehensive Algorithm Works")
    st.markdown("""
    * **Industrial Capacity Ceiling & Penalties:** Reindustrialising up to €6B drives growth and resilience, but pushing past €6B triggers diminishing returns, grid stress, carbon regulatory penalties, and civil friction—explaining the historical caution behind deindustrialisation.
    * **Medical Sovereignty & Talent Retention:** Balances national health security and stops high-skill brain drain.
    * **Monetary & Demographic Constraints:** Incorporates dynamic ECB interest rates and ageing population pension liabilities over 10 years.
    """)
