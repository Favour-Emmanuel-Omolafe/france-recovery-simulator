# 🇫🇷 France 2030: Macroeconomic Crisis Simulator

![Dashboard Screenshot 1](phase%201.png)
![Dashboard Screenshot 2](phase%202.png)
![Dashboard Screenshot 3](phase%203.png)
![Dashboard Screenshot 4](phase%204.png)

# 🇫🇷 France 2026-2036: Comprehensive Crisis & Solution Optimiser

> A data-driven macro-simulation web app exploring the complex trade-offs of fiscal consolidation, industrial reshoring, brain drain, and public unrest in France.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-red?logo=streamlit)](https://france-recovery-simulator-jxtd7fwuam65yqhyfsg5as.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)

---

## 🚀 Live Demo
Experience the interactive simulation live in your browser:  
👉 **[Launch France 2030 Simulator](https://france-recovery-simulator-jxtd7fwuam65yqhyfsg5as.streamlit.app/)**

---

## 📌 Project Overview
France faces a severe macroeconomic trilemma: soaring public debt (>110% of GDP), excessive deficits breaching EU limits (3%), structural "smicardization" of wages, and the constant threat of social unrest or general strikes. 

This project moves beyond passive economic forecasting to become a **prescriptive policy engine**. It lets users pilot France’s fiscal, industrial, and social levers over a 10-year horizon (2026–2036) to find an effective policy mix to achieve economic stability without igniting civil unrest.

---

## 🧠 Core Modeling & Mechanics
The custom simulation engine models complex, non-linear economic dynamics:

1. **Monetary Policy Constraint (ECB Integration):** 
   * Incorporates the European Central Bank's baseline interest rates and dynamic risk spreads. Even with a domestically balanced budget, high ECB interest costs can trigger debt spirals.
2. **Demographic Pension Compounding:** 
   * Simulates the compounding fiscal impact of an ageing population for pension liabilities over the 10-year period, and shows how raising the statutory retirement age yields non-linear savings.
3. **The Industrial Capacity Ceiling & Carbon Penalties:** 
   * Reindustrialisation up to €6B drives clean GDP growth and supports regional jobs. However, pushing past €6B triggers diminishing returns, energy grid strain, and carbon regulatory fines.
4. **Tax-Driven Brain Drain Logic:** 
   * Raising general corporate and high-earner taxes excessively necessarily degrades retention of top-tier talent, simulating international talent flight.
5. **The Automated AI Solver:** 
   * Features a built-in optimiser that scans thousands of policy combinations to find automatically the optimal path to meet the 3% deficit target without crossing the 75-point general strike threshold.

---

## 🛠️ Interactive Policy Levers

* **🌍 Global Macro Shocks:** Set ECB interest rates, simulate fuel/energy scarcity shocks, and toggle global geopolitical conflicts.
* **🏛️ French Political Levers:** Adjust statutory retirement age and reinstate wealth tax (ISF).
* **🏗️ Structural Growth Levers (€B):** 
  * *Industrial Reshoring & Factories* (rebuilding domestic manufacturing)
  * *Medical & Pharma Production* (securing local healthcare supply chains)
  * *Top-Tier Talent Retention & R&D* (combating brain drain)
* **💼 Standard Fiscal Levers (€B):** Manage tech investments, administrative savings, public job cuts, and corporate tax relief.
* **🛡️ Social Buffers (€B):** Fund hospital investments and youth/student grants to suppress civil grievance.

---

## 📊 Outputs & Dashboard Analytics
* **Real-Time Macro Metrics:** Tracks 2036 Debt-to-GDP, Deficit compliance, GDP growth, and a **Strike Risk Speedometer**.
* **Deficit Waterfall Bridge:** A custom Plotly waterfall visualisation breaking down the exact contribution of baseline adjustments, austerity, pension reforms, and macroeconomic growth dynamics.
* **Long-Term Trajectory Charts:** Multi-year line charts tracking public debt, annual GDP growth, and social unrest index.

---

## 💻 Local Installation & Setup

If you want to run or test this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/france-recovery-simulator.git](https://github.com/YourUsername/france-recovery-simulator.git)
   cd france-recovery-simulator
