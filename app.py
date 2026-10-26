import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import itertools

st.set_page_config(page_title="France 2030 Simulator", layout="wide")

# 1. The Core Engine (Fixed for Realistic Debt Dynamics)
def simulate_economy(admin_cut, pension_cut, job_cut, tax_cut, hosp_inv, youth_grant, tech_inv, fuel_scarcity_lvl, war_shock, horizon=10):
    years = [2026 + i for i in range(horizon + 1)]
    debt, deficit, unrest, gdp = np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1)
    
    # Oct 2026 Current Crisis Baseline
    debt[0], deficit[0], unrest[0], gdp[0] = 120.0, 5.4, 55.0, 0.4 
    nom_gdp = 3100.0

    for t in range(horizon):
        # Unrest Calculation
        grievance = 55.0 + (admin_cut * 0.3) + (pension_cut * 1.8) + (job_cut * 3.5) + (tax_cut * 0.6)
        grievance += (fuel_scarcity_lvl * 4.0) 
        grievance -= (hosp_inv * 2.0) + (youth_grant * 1.5) + (tech_inv * 0.5)
        
        unrest[t+1] = np.clip(0.6 * unrest[t] + 0.4 * grievance, 0, 100)
        strike_drag = 0.8 if unrest[t+1] >= 75.0 else 0.0
        
        # GDP Multipliers
        war_drag = 0.4 if war_shock else 0.0
        fuel_drag = fuel_scarcity_lvl * 0.15
        
        gdp[t+1] = 0.4 + (tax_cut * 0.05) + (tech_inv * 0.08) - (job_cut * 0.05) - fuel_drag - war_drag - strike_drag
        
        # Fiscal Balance & Deficit
        real_job_savings = job_cut * 0.5 # Unemployment benefit drag
        net_effort = admin_cut + pension_cut + real_job_savings - hosp_inv - youth_grant - tax_cut - tech_inv
        
        fiscal_pct = (net_effort / nom_gdp) * 100.0
        growth_div = (gdp[t+1] - 0.4) * 0.4
        deficit[t+1] = np.clip(deficit[t] - fiscal_pct - growth_div, 1.0, 12.0)
        
        # REALISTIC DEBT DYNAMICS
        war_premium = 20.0 if war_shock else 0.0
        spread = 35.0 + (10.0 * max(0, deficit[t+1] - 3.0)) + (0.5 * unrest[t+1]) + war_premium
        
        g_nom = (gdp[t+1] + 2.0) / 100.0 
        debt_reduction_from_growth = debt[t] * g_nom
        debt[t+1] = debt[t] + deficit[t+1] - debt_reduction_from_growth
        
    return pd.DataFrame({'Year': years, 'Debt_GDP': debt, 'Deficit_GDP': deficit, 'Unrest_Index': unrest, 'GDP_Growth': gdp})

# 2. The Auto-Solver
def find_optimal_solution(current_fuel, current_war):
    best_combo = None
    lowest_unrest = 100
    
    admin = range(0, 6, 1)  
    pension = range(0, 16, 5)
    job = range(0, 11, 2)
    tax = range(0, 11, 2)
    
    for a, p, j, t in itertools.product(admin, pension, job, tax):
        h_inv, y_grant, tech_inv = 3.0, 2.0, 3.0 
        df_sim = simulate_economy(a, p, j, t, h_inv, y_grant, tech_inv, current_fuel, current_war)
        d_def, d_unrest = df_sim['Deficit_GDP'].iloc[-1], df_sim['Unrest_Index'].iloc[-1]
        
        if d_def <= 3.0 and d_unrest < 75.0:
            if d_unrest < lowest_unrest:
                lowest_unrest = d_unrest
                best_combo = (a, p, j, t, h_inv, y_grant, tech_inv, d_def, d_unrest)
                
    return best_combo

# 3. Sidebar UI
st.sidebar.markdown("### 🇫🇷 France 2030 Optimizer\n**Built by Favour Emmanuel Omolafe**\n---")

fuel_shock = st.sidebar.slider("🌍 Fuel Scarcity & Energy Shock (0-5)", 0.0, 5.0, st.session_state.get('fuel', 0.0), step=1.0)
war_toggle = st.sidebar.checkbox("🌍 Global Geopolitical Conflict", value=st.session_state.get('war', False))

if st.sidebar.button("🤖 Auto-Solve for 3% Deficit (AI Optimizer)"):
    with st.spinner("Calculating global shock impacts & optimal policies..."):
        optimal = find_optimal_solution(fuel_shock, war_toggle)
        if optimal:
            st.sidebar.success("Optimal Solution Found!")
            for idx, key in enumerate(['admin', 'pension', 'job', 'tax', 'hosp', 'youth', 'tech']):
                st.session_state[key] = float(optimal[idx])
        else:
            st.sidebar.error("CRITICAL: Global shocks too severe. No mathematical solution exists.")

st.sidebar.header("Economic & Tech Levers (€B)")
tech_invest = st.sidebar.slider("Industrial & Tech Investment", 0.0, 10.0, st.session_state.get('tech', 2.0), step=1.0)
admin_cuts = st.sidebar.slider("Admin Savings", 0.0, 5.0, st.session_state.get('admin', 2.0), step=1.0)
pension_cuts = st.sidebar.slider("Pension Cuts", 0.0, 20.0, st.session_state.get('pension', 0.0), step=1.0)
public_job_cuts = st.sidebar.slider("Job Cuts", 0.0, 15.0, st.session_state.get('job', 0.0), step=1.0)
corporate_tax_cuts = st.sidebar.slider("Tax Cuts", 0.0, 20.0, st.session_state.get('tax', 0.0), step=1.0)

st.sidebar.header("Social Buffers (€B)")
hospital_inv = st.sidebar.slider("Hospital Invest", 0.0, 10.0, st.session_state.get('hosp', 3.0), step=0.5)
student_budget = st.sidebar.slider("Youth Grants", 0.0, 10.0, st.session_state.get('youth', 2.0), step=0.5)

# Run Simulation
df_results = simulate_economy(admin_cuts, pension_cuts, public_job_cuts, corporate_tax_cuts, hospital_inv, student_budget, tech_invest, fuel_shock, war_toggle)
final_debt, final_def, final_unrest, final_gdp = df_results.iloc[-1][['Debt_GDP', 'Deficit_GDP', 'Unrest_Index', 'GDP_Growth']]

# Main UI
st.title("🇫🇷 France 2026-2036: Crisis Optimizer")

# Executive Banner at the top
if final_def <= 3.0 and final_unrest < 75:
    st.success(f"🏆 MACROECONOMIC TRILEMMA SOLVED: Deficit stabilized at {final_def:.1f}% without triggering riots.")
elif final_unrest >= 75:
    st.error(f"🔥 GENERAL STRIKE: Strike Index hit {final_unrest:.1f}. The economy has shut down due to severe austerity.")
elif final_def > 3.0:
    st.warning(f"📉 DEBT SPIRAL: Deficit is {final_def:.1f}%. The EU has rejected your budget. Markets are panicking.")

tab1, tab2 = st.tabs(["📊 Live Simulator", "🧠 Model Methodology"])

with tab1:
    with st.expander("💡 Executive Summary & Usage"):
        st.write("Adjust the economic levers on the left to find €60B in savings. Your goal is to get the 2036 Deficit under 3.0% without pushing the Strike Risk Index over 75.")
        
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("2036 Debt-to-GDP", f"{final_debt:.1f}%")
    col2.metric("2036 Deficit", f"{final_def:.1f}%", "EU Compliant" if final_def <= 3.0 else "Violation", delta_color="inverse")
    col3.metric("Strike Risk Index", f"{final_unrest:.1f}", "STRIKE TRIGGERED" if final_unrest >= 75 else "Stable", delta_color="inverse")
    col4.metric("2036 GDP Growth", f"{final_gdp:.1f}%")

    st.markdown("---")
    
    # Interactive Plotly Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig1 = px.line(df_results, x='Year', y='Deficit_GDP', title='Budget Deficit (% of GDP)', markers=True, color_discrete_sequence=['#ff4b4b'])
        fig1.add_hline(y=3.0, line_dash="dot", annotation_text="EU 3% Limit", annotation_position="bottom right")
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.line(df_results, x='Year', y='Debt_GDP', title='Gross Public Debt (% of GDP)', markers=True, color_discrete_sequence=['#0068c9'])
        st.plotly_chart(fig2, use_container_width=True)

    with col_chart2:
        fig3 = px.line(df_results, x='Year', y='Unrest_Index', title='Social Unrest Index', markers=True, color_discrete_sequence=['#ffaa00'])
        fig3.add_hline(y=75.0, line_dash="dot", annotation_text="General Strike Threshold", annotation_position="bottom right")
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.line(df_results, x='Year', y='GDP_Growth', title='Annual GDP Growth (%)', markers=True, color_discrete_sequence=['#29b09d'])
        st.plotly_chart(fig4, use_container_width=True)

    # Export Button
    csv = df_results.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Scenario Data (CSV)", data=csv, file_name='france_simulation_results.csv', mime='text/csv')

with tab2:
    st.header("How the Algorithm Works")
    st.markdown("""
    * **Fiscal Multipliers:** Slashing jobs reduces the deficit but directly penalizes GDP.
    * **Strike Risk:** An algorithmic threshold (0-100). If it crosses 75, a 'General Strike' penalty is applied to GDP.
    * **Unemployment Drag:** Every €1B cut in jobs only yields €0.5B in net savings due to welfare payouts.
    * **Global Shocks:** War and Fuel Scarcity act as external penalties to growth and inflation, forcing you to adjust domestic policy to compensate.
    * **Realistic Debt Dynamics:** Economic growth dynamically reduces the debt-to-GDP ratio, while budget deficits and bond yields compound it over time.
    """)
