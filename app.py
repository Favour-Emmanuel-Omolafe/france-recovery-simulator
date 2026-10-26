import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

st.set_page_config(page_title="France 2030 Simulator", layout="wide")

# 1. The Core Engine (Wired for October 2026 Reality)
def simulate_economy(admin_cut, pension_cut, job_cut, tax_cut, hosp_inv, youth_grant, horizon=10):
    debt, deficit, unrest, gdp = np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1), np.zeros(horizon+1)
    
    # Oct 2026 Current Crisis Baseline
    debt[0], deficit[0], unrest[0], gdp[0] = 120.0, 5.4, 55.0, 0.4 
    nom_gdp = 3100.0

    for t in range(horizon):
        # Unrest Calculation (Highly sensitive to job & pension cuts)
        grievance = 55.0 + (admin_cut * 0.3) + (pension_cut * 1.8) + (job_cut * 3.0) + (tax_cut * 0.6)
        grievance -= (hosp_inv * 2.0) + (youth_grant * 1.5)
        
        unrest[t+1] = np.clip(0.6 * unrest[t] + 0.4 * grievance, 0, 100)
        strike_drag = 0.8 if unrest[t+1] >= 75.0 else 0.0
        
        # GDP Multipliers
        gdp[t+1] = 0.4 + (tax_cut * 0.05) - (job_cut * 0.03) - strike_drag
        
        # Fiscal Balance
        net_effort = admin_cut + pension_cut + job_cut - hosp_inv - youth_grant - tax_cut
        fiscal_pct = (net_effort / nom_gdp) * 100.0
        growth_div = (gdp[t+1] - 0.4) * 0.4
        
        deficit[t+1] = np.clip(deficit[t] - fiscal_pct - growth_div, 1.0, 9.0)
        
        # Debt Snowball
        spread = 35.0 + (10.0 * max(0, deficit[t+1] - 3.0)) + (0.5 * unrest[t+1])
        r_eff = (2.8 + (spread / 100.0)) / 100.0
        g_nom = (gdp[t+1] + 2.0) / 100.0
        debt[t+1] = debt[t] * ((1.0 + r_eff) / (1.0 + g_nom)) + deficit[t+1]
        
    return debt[-1], deficit[-1], unrest[-1], gdp[-1]

# 2. The Auto-Solver (Prescriptive Analytics)
def find_optimal_solution():
    best_combo = None
    lowest_unrest = 100
    
    # Test combinations of policies
    admin = range(0, 31, 5)
    pension = range(0, 16, 5)
    job = range(0, 11, 2)
    tax = range(0, 11, 2)
    
    for a, p, j, t in itertools.product(admin, pension, job, tax):
        # Always maintain a minimum social buffer
        h_inv, y_grant = 3.0, 2.0 
        d_debt, d_def, d_unrest, d_gdp = simulate_economy(a, p, j, t, h_inv, y_grant)
        
        # Win Condition: Deficit under 3%, no strikes
        if d_def <= 3.0 and d_unrest < 75.0:
            if d_unrest < lowest_unrest:
                lowest_unrest = d_unrest
                best_combo = (a, p, j, t, h_inv, y_grant, d_def, d_unrest)
                
    return best_combo

# 3. UI Setup
st.title("🇫🇷 France 2026-2036: Crisis Optimizer")
st.markdown("Current baseline: October 2026. Deficit is 5.4%. Debt is 120%. Youth unrest is rising. You must find €60B in adjustments to hit the EU 3% limit without triggering a general strike.")

st.sidebar.markdown("**Built by Favour Emmanuel Omolafe**\n---")

# The "Magic" Button
if st.sidebar.button("🤖 Auto-Solve for 3% Deficit (AI Optimizer)"):
    with st.spinner("Testing thousands of policy combinations..."):
        optimal = find_optimal_solution()
        if optimal:
            st.sidebar.success("Optimal Solution Found!")
            st.session_state['admin'] = float(optimal[0])
            st.session_state['pension'] = float(optimal[1])
            st.session_state['job'] = float(optimal[2])
            st.session_state['tax'] = float(optimal[3])
            st.session_state['hosp'] = float(optimal[4])
            st.session_state['youth'] = float(optimal[5])
        else:
            st.sidebar.error("No safe solution exists. Mathematical collapse inevitable.")

# Sliders (Linked to session state for the Auto-Solver)
st.sidebar.header("Adjust Policies (€B)")
admin_cuts = st.sidebar.slider("Admin Savings", 0.0, 30.0, st.session_state.get('admin', 10.0), step=1.0)
pension_cuts = st.sidebar.slider("Pension Cuts", 0.0, 20.0, st.session_state.get('pension', 0.0), step=1.0)
public_job_cuts = st.sidebar.slider("Job Cuts", 0.0, 15.0, st.session_state.get('job', 0.0), step=1.0)
corporate_tax_cuts = st.sidebar.slider("Tax Cuts", 0.0, 20.0, st.session_state.get('tax', 0.0), step=1.0)
hospital_inv = st.sidebar.slider("Hospital Invest", 0.0, 10.0, st.session_state.get('hosp', 3.0), step=0.5)
student_budget = st.sidebar.slider("Youth Grants", 0.0, 10.0, st.session_state.get('youth', 2.0), step=0.5)

# Run Simulation
final_debt, final_def, final_unrest, final_gdp = simulate_economy(admin_cuts, pension_cuts, public_job_cuts, corporate_tax_cuts, hospital_inv, student_budget)

# Display Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("2036 Debt-to-GDP", f"{final_debt:.1f}%")
col2.metric("2036 Deficit", f"{final_def:.1f}%", "EU Compliant" if final_def <= 3.0 else "Violation", delta_color="inverse")
col3.metric("Strike Risk Index", f"{final_unrest:.1f}", "STRIKE TRIGGERED" if final_unrest >= 75 else "Stable", delta_color="inverse")
col4.metric("2036 GDP Growth", f"{final_gdp:.1f}%")

if final_def <= 3.0 and final_unrest < 75:
    st.success("🏆 MACROECONOMIC TRILEMMA SOLVED: You stabilized the debt without triggering riots.")
elif final_unrest >= 75:
    st.error("🔥 GENERAL STRIKE: The economy has shut down due to severe austerity.")
elif final_def > 3.0:
    st.warning("📉 DEBT SPIRAL: The EU has rejected your budget. Markets are panicking.")
