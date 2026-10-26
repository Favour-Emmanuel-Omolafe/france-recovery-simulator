import streamlit as st
import pandas as pd
import numpy as np
import itertools

st.set_page_config(page_title="France 2026-2036 Crisis Optimizer", layout="wide")

# 1. Core Economic Simulation Engine
def simulate_economy(admin_cuts, pension_cuts, public_job_cuts, corporate_tax_cuts, hospital_inv, student_budget, tech_invest, fuel_shock, war_toggle):
    years = range(2026, 2037)
    
    # Baseline dynamics
    base_debt = 112.0
    base_deficit = 5.5
    base_unrest = 30.0
    base_gdp = 1.1
    
    debt = []
    deficit = []
    unrest = []
    gdp = []
    
    current_debt = base_debt
    current_unrest = base_unrest
    
    for i, year in enumerate(years):
        # Fiscal and structural impacts
        total_savings = admin_cuts + (pension_cuts * 0.6) + (public_job_cuts * 0.5) - (corporate_tax_cuts * 0.4)
        social_buffers = hospital_inv + student_budget + tech_invest
        
        # Deficit calculation
        net_fiscal_adjustment = total_savings - social_buffers
        current_deficit = max(1.0, base_deficit - (net_fiscal_adjustment * 0.4) + (fuel_shock * 0.3) + (2.0 if war_toggle else 0.0))
        
        # GDP Growth calculation
        growth = max(-1.5, base_gdp + (corporate_tax_cuts * 0.05) - (admin_cuts * 0.03) + (tech_invest * 0.08) - (fuel_shock * 0.2) - (1.0 if war_toggle else 0.0))
        
        # Unrest calculation
        unrest_delta = (pension_cuts * 1.5) + (public_job_cuts * 1.2) - (hospital_inv * 1.0) - (student_budget * 0.8) + (fuel_shock * 4.0) + (15.0 if war_toggle else 0.0)
        current_unrest = min(100.0, max(10.0, current_unrest * 0.8 + unrest_delta * 0.2))
        
        # Debt calculation
        current_debt = current_debt + current_deficit - growth
        
        debt.append(round(current_debt, 1))
        deficit.append(round(current_deficit, 1))
        unrest.append(round(current_unrest, 1))
        gdp.append(round(growth, 1))
        
    return pd.DataFrame({
        'Year': years, 
        'Debt_GDP': debt, 
        'Deficit_GDP': deficit, 
        'Unrest_Index': unrest, 
        'GDP_Growth': gdp
    })

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

fuel_shock = st.sidebar.slider(
    "🌍 Fuel Scarcity & Energy Shock (0-5)", 
    0.0, 5.0, 
    st.session_state.get('fuel', 0.0), 
    step=1.0, 
    help="Simulates severity of energy supply bottlenecks and public fuel shortages."
)

war_toggle = st.sidebar.checkbox("⚔️ Geopolitical Escalation / European Conflict", value=st.session_state.get('war', False))

st.sidebar.header("Austerity Levers (€B)")
admin_cuts = st.sidebar.slider(
    "Admin Savings", 
    0.0, 5.0, 
    st.session_state.get('admin', 2.0), 
    step=1.0, 
    help="Cuts to government operating expenses to quickly reduce the deficit."
)
pension_cuts = st.sidebar.slider(
    "Pension Cuts", 
    0.0, 20.0, 
    st.session_state.get('pension', 0.0), 
    step=1.0, 
    help="Adjusts retirement spending. High cuts heavily increase the Strike Risk Index."
)
public_job_cuts = st.sidebar.slider(
    "Job Cuts", 
    0.0, 15.0, 
    st.session_state.get('job', 0.0), 
    step=1.0, 
    help="Downsizes public sector employment to save funds."
)
corporate_tax_cuts = st.sidebar.slider(
    "Tax Cuts", 
    0.0, 20.0, 
    st.session_state.get('tax', 0.0), 
    step=1.0, 
    help="Lowers business taxes to encourage corporate investment."
)

st.sidebar.header("Social Buffers (€B)")
hospital_inv = st.sidebar.slider(
    "Hospital Invest", 
    0.0, 10.0, 
    st.session_state.get('hosp', 3.0), 
    step=0.5, 
    help="Increases healthcare funding to absorb social pressure and lower unrest."
)
student_budget = st.sidebar.slider(
    "Youth Grants", 
    0.0, 10.0, 
    st.session_state.get('youth', 2.0), 
    step=0.5, 
    help="Provides financial support to students to prevent youth-led protests."
)
tech_invest = 3.0

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
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI Metrics with informative tooltips
    col1.metric("Final Debt (% GDP)", f"{final_debt:.1f}%", help="Projected national debt ratio relative to total GDP by 2036.")
    col2.metric("Final Deficit (% GDP)", f"{final_def:.1f}%", delta=f"{final_def - 5.5:.1f}% vs base", help="Annual budget deficit. EU rules target staying below 3.0%.")
    
    # Dynamic Strike Risk Status Formatting
    unrest_status = "Stable"
    if final_unrest >= 75:
        unrest_status = "General Strike 🔥"
    elif final_unrest >= 40:
        unrest_status = "High Tension ⚠️"
        
    col3.metric("Strike Risk Index", f"{final_unrest:.1f}/100", delta=unrest_status, delta_color="inverse", help="Measures socio-political friction and likelihood of labor shutdowns (0-100 scale).")
    col4.metric("Avg GDP Growth", f"{final_gdp:.1f}%", help="Average annualized economic growth over the simulation period.")

    st.line_chart(df_results.set_index('Year')[['Debt_GDP', 'Deficit_GDP', 'Unrest_Index']])

with tab2:
    st.subheader("Methodology & Behavioral Modeling")
    st.write("This simulation model evaluates fiscal policy trade-offs in France, balancing debt reduction against social stability and growth multipliers.")

# Auto-solver button in sidebar
if st.sidebar.button("🤖 Run Auto-Solver"):
    best = find_optimal_solution(fuel_shock, war_toggle)
    if best:
        st.sidebar.success(f"Optimal Solution Found!\nAdmin: {best[0]}, Pension: {best[1]}, Jobs: {best[2]}, Tax: {best[3]}")
    else:
        st.sidebar.error("No combination met the targets under current shocks.")
