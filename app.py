import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

st.set_page_config(page_title="France 2030 Simulator", layout="wide")

# 1. The Core Engine (Now with Global Shocks & Industrial Tech Investments)
def simulate_economy(admin_cut, pension_cut, job_cut, tax_cut, hosp_inv, youth_grant, tech_inv, fuel_scarcity_lvl, war_shock, horizon=10):
    debt, deficit, unrest, gdp = np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1)
    
    # Oct 2026 Current Crisis Baseline
    debt[0], deficit[0], unrest[0], gdp[0] = 120.0, 5.4, 55.0, 0.4 
    nom_gdp = 3100.0

    for t in range(horizon):
        # Unrest: Fuel scarcity triggers massive anger (The Yellow Vest Effect)
        grievance = 55.0 + (admin_cut * 0.3) + (pension_cut * 1.8) + (job_cut * 3.5) + (tax_cut * 0.6)
        grievance += (fuel_scarcity_lvl * 4.0) 
        grievance -= (hosp_inv * 2.0) + (youth_grant * 1.5) + (tech_inv * 0.5) # Tech jobs create hope
        
        unrest[t+1] = np.clip(0.6 * unrest[t] + 0.4 * grievance, 0, 100)
        strike_drag = 0.8 if unrest[t+1] >= 75.0 else 0.0
        
        # GDP Multipliers: War & Fuel kill growth; Tech Investment compounds it
        war_drag = 0.4 if war_shock else 0.0
        fuel_drag = fuel_scarcity_lvl * 0.15
        
        gdp[t+1] = 0.4 + (tax_cut * 0.05) + (tech_inv * 0.08) - (job_cut * 0.05) - fuel_drag - war_drag - strike_drag
        
        # Unemployment Drag
        real_job_savings = job_cut * 0.5
        
        # Fiscal Balance (Tech investment costs money upfront)
        net_effort = admin_cut + pension_cut + real_job_savings - hosp_inv - youth_grant - tax_cut - tech_inv
        fiscal_pct = (net_effort / nom_gdp) * 100.0
        growth_div = (gdp[t+1] - 0.4) * 0.4
        
        deficit[t+1] = np.clip(deficit[t] - fiscal_pct - growth_div, 1.0, 12.0)
        
        # Debt Snowball: War panics the bond markets
        war_premium = 20.0 if war_shock else 0.0
        spread = 35.0 + (10.0 * max(0, deficit[t+1] - 3.0)) + (0.5 * unrest[t+1]) + war_premium
        r_eff = (2.8 + (spread / 100.0)) / 100.0
        g_nom = (gdp[t+1] + 2.0) / 100.0
        debt[t+1] = debt[t] * ((1.0 + r_eff) / (1.0 + g_nom)) + deficit[t+1]
        
    return debt[-1], deficit[-1], unrest[-1], gdp[-1]

# 2. The Auto-Solver (Now adapts to global conditions)
def find_optimal_solution(current_fuel, current_war):
    best_combo = None
    lowest_unrest = 100
    
    admin = range(0, 6, 1)  
    pension = range(0, 16, 5)
    job = range(0, 11, 2)
    tax = range(0, 11, 2)
    
    for a, p, j, t in itertools.product(admin, pension, job, tax):
        h_inv, y_grant, tech_inv = 3.0, 2.0, 3.0 # Maintain basic social & tech buffers
        d_debt, d_def, d_unrest, d_gdp = simulate_economy(a, p, j, t, h_inv, y_grant, tech_inv, current_fuel, current_war)
        
        if d_def <= 3.0 and d_unrest < 75.0:
            if d_unrest < lowest_unrest:
                lowest_unrest = d_unrest
                best_combo = (a, p, j, t, h_inv, y_grant, tech_inv, d_def, d_unrest)
                
    return best_combo

# 3. UI Setup
st.title("🇫🇷 France 2026-2036: Crisis Optimizer")
st.markdown("Navigate domestic budget cuts while surviving global energy shocks and geopolitical conflicts. Generate long-term cash flow via Tech Investments.")

st.sidebar.markdown("**Built by Favour Emmanuel Omolafe**\n---")

# Global variables read first for the AI
fuel_shock = st.sidebar.slider("🌍 Fuel Scarcity & Energy Shock (0-5)", 0.0, 5.0, st.session_state.get('fuel', 0.0), step=1.0, help="Drives up inflation, triggering massive citizen unrest and slowing industry.")
war_toggle = st.sidebar.checkbox("🌍 Global Geopolitical Conflict", value=st.session_state.get('war', False), help="Disrupts supply chains (GDP drop) and panics bond markets (Yield spike).")

if st.sidebar.button("🤖 Auto-Solve for 3% Deficit (AI Optimizer)"):
    with st.spinner("Calculating global shock impacts & optimal policies..."):
        optimal = find_optimal_solution(fuel_shock, war_toggle)
        if optimal:
            st.sidebar.success("Optimal Solution Found for this Global Climate!")
            st.session_state['admin'] = float(optimal[0])
            st.session_state['pension'] = float(optimal[1])
            st.session_state['job'] = float(optimal[2])
            st.session_state['tax'] = float(optimal[3])
            st.session_state['hosp'] = float(optimal[4])
            st.session_state['youth'] = float(optimal[5])
            st.session_state['tech'] = float(optimal[6])
        else:
            st.sidebar.error("CRITICAL: The global shocks are too severe. No mathematical solution exists without a general strike or EU default.")

st.sidebar.header("Economic & Tech Levers (€B)")
tech_invest = st.sidebar.slider("Industrial & Tech Investment", 0.0, 10.0, st.session_state.get('tech', 2.0), step=1.0, help="Costs money upfront but compounds GDP growth and competitiveness over 10 years.")
admin_cuts = st.sidebar.slider("Admin Savings", 0.0, 5.0, st.session_state.get('admin', 2.0), step=1.0)
pension_cuts = st.sidebar.slider("Pension Cuts", 0.0, 20.0, st.session_state.get('pension', 0.0), step=1.0)
public_job_cuts = st.sidebar.slider("Job Cuts", 0.0, 15.0, st.session_state.get('job', 0.0), step=1.0)
corporate_tax_cuts = st.sidebar.slider("Tax Cuts", 0.0, 20.0, st.session_state.get('tax', 0.0), step=1.0)

st.sidebar.header("Social Buffers (€B)")
hospital_inv = st.sidebar.slider("Hospital Invest", 0.0, 10.0, st.session_state.get('hosp', 3.0), step=0.5)
student_budget = st.sidebar.slider("Youth Grants", 0.0, 10.0, st.session_state.get('youth', 2.0), step=0.5)

# Run Simulation
final_debt, final_def, final_unrest, final_gdp = simulate_economy(admin_cuts, pension_cuts, public_job_cuts, corporate_tax_cuts, hospital_inv, student_budget, tech_invest, fuel_shock, war_toggle)

# Display Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("2036 Debt-to-GDP", f"{final_debt:.1f}%")
col2.metric("2036 Deficit", f"{final_def:.1f}%", "EU Compliant" if final_def <= 3.0 else "Violation", delta_color="inverse")
col3.metric("Strike Risk Index", f"{final_unrest:.1f}", "STRIKE TRIGGERED" if final_unrest >= 75 else "Stable", delta_color="inverse")
col4.metric("2036 GDP Growth", f"{final_gdp:.1f}%")

if final_def <= 3.0 and final_unrest < 75:
    st.success("🏆 MACROECONOMIC TRILEMMA SOLVED: You stabilized the debt without triggering riots.")
elif final_unrest >= 75:
    st.error("🔥 GENERAL STRIKE: The economy has shut down due to severe austerity and inflation.")
elif final_def > 3.0:
    st.warning("📉 DEBT SPIRAL: The EU has rejected your budget. Markets are panicking.")
