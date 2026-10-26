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
        
        # REALISTIC DEBT DYNAMICS (The Fix)
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
public_job_cuts = st.sidebar
