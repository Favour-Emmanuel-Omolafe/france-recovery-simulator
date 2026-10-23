# 🇫🇷 France 2030+: Macro-Fiscal & Democratic Recovery Simulator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Data Science](https://img.shields.io/badge/Domain-Macroeconomics-green.svg)]()

👉 **[Click here to launch the Live Interactive Simulator](YOUR_STREAMLIT_LINK)**

## 📌 Executive Summary
France currently faces a critical macroeconomic trilemma: the mathematical necessity of reducing a €3.54 trillion public debt, the economic reality of sluggish GDP growth, and the social reality that severe austerity triggers paralysing nationwide strikes.

This project is a **Python-based interactive simulation engine** built to stress-test fiscal consolidation strategies. It lets policymakers and analysts adjust economic levers and instantly model the 10-year impact on national debt, budget deficit, GDP growth, and a calculated "Strike Risk Index."

## ⚙️ The Macroeconomic Engine
Unlike static financial models, this algorithm accounts for dynamic human behaviour and fiscal multipliers over a 10-year horizon (2026–2036). 

The engine calculates the cascading effects of policy decisions:
* **The Fiscal Multiplier Effect:** Slashing public sector jobs reduces the deficit but directly penalises GDP growth (as consumption drops) and spikes social unrest. Conversely, corporate tax cuts increase the short-term deficit but stimulate long-term GDP growth via business investment.
* **The Strike Risk Index (0-100):** A custom algorithmic threshold. If unpopular policies (like pension cuts or bypassing parliament via Article 49.3) push the index above 75, the model triggers a "General Strike Drag," severely reducing GDP growth and widening the bond yield spread.
* **Market Panic (OAT Spread):** Bond yields react dynamically. If the deficit breaches the EU's 3% limit or social unrest spirals, the model increases borrowing costs, accelerating the debt snowball.

## 📊 Key Features & Interactive Levers
The Streamlit dashboard allows users to adjust real-world policies to find the mathematical "Social Compact" required to save the economy:
- **Economic & Fiscal:** Administrative Savings, Public Sector Job Cuts, Pension Reform, Corporate Tax Cuts.
- **Social & Demographic:** Hospital Reinvestment, Student/Youth Grants, Net Labour Integration.
- **Political:** Bypassing Parliament (Article 49.3), Union Pacts, Geopolitical Shocks.

## 🛠️ Technical Stack
* **Language:** Python
* **Frontend/UI:** Streamlit
* **Data Processing:** NumPy, pandas
* **Data Visualisation:** Matplotlib, Seaborn (Custom styling for executive reporting)

## 💻 Local Installation & Usage
To run this simulator on your local machine:

1. Clone the repository:
   ```bash
   git clone [https://github.com/Favour-Emmanuel-Omolafe/france-recovery-simulator.git](https://github.com/Favour-Emmanuel-Omolafe/france-recovery-simulator.git)
   cd france-recovery-simulator
