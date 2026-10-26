# 🇫🇷 France 2026-2036: Macro-Fiscal Crisis Optimiser

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Data Science](https://img.shields.io/badge/Domain-Macroeconomics-green.svg)]()

👉 [Click here to launch the Live Interactive Simulator](https://share.streamlit.io/)

## 📌 Executive Summary
As of October 2026, France faces a severe macroeconomic trilemma: a bloated national debt (120% of GDP), a budget deficit of 5.4% (violating EU limits), and a highly volatile social climate where aggressive austerity measures risk triggering nationwide strikes. 

This project is a **Python-based interactive prescriptive analytics engine** built to address this exact crisis. It allows policymakers and analysts to stress-test €60B in budget adjustments, mapping the cascading effects on GDP growth, debt trajectory, and social stability over a 10-year horizon.

## ⚙️ The Macroeconomic Engine
Unlike static financial spreadsheets, this algorithm accounts for the dynamic human behaviour and fiscal multipliers.
* **The Fiscal Multiplier Effect:** The fiscal multiplier effect means that slashing public sector jobs reduces the deficit, but directly penalises GDP growth (as consumption drops). Conversely, corporate tax cuts increase the short-term deficit; however, they stimulate long-term GDP growth via business investment.
* **The Strike Risk Index (0–100):** A custom algorithm-based threshold. If unpopular policies (like pension cuts or public sector layoffs) push the index above 75, the model triggers a "General Strike Drag," severely reducing GDP growth and widening the bond yield spread.
* **Market Panic (OAT Spread):** Bond yields react dynamically. If the deficit breaches the EU's 3% limit or social unrest spirals, borrowing costs mathematically increase, accelerating the debt snowball.

## 🤖 The AI Auto-Solver (Prescriptive Analytics)
This simulator moves from descriptive to **prescriptive analytics** with a built-in optimisation engine. Using Python's `itertools`, the application tests thousands of policy combinations in the background to find the optimal fiscal path. 

With one click, it mathematically hunts for the optimal combination of tax cuts, budget cuts, and social investments required to reduce the deficit below the EU's 3% limit by 2036 *without* triggering a general strike.

## 📊 Interactive Policy Levers
- **Economic & Fiscal Adjustments:** Administrative Savings, Public Sector Job Cuts, Pension Reform, Corporate Tax Cuts.
- **Social & Demographic Buffers:** Hospital Reinvestment, Student and Youth Grants.

## 🛠️ Technical Stack
* **Language:** Python
* **Frontend/UI:** Streamlit
* **Data Processing:** NumPy, pandas
* **Optimization Engine:** Itertools (Combinatorial optimization)
* **Data Visualization:** Matplotlib, Seaborn

## 💻 Local Installation & Usage
To run this simulator on your local machine:

1. Clone the repository:
   ```bash
   git clone [https://github.com/Favour-Emmanuel-Omolafe/france-recovery-simulator.git](https://github.com/Favour-Emmanuel-Omolafe/france-recovery-simulator.git)
   cd france-recovery-simulator
```

   
## 🧠 Model Methodology & Behavioral Logic
The **France 2026-2036 Crisis Optimiser ** simulates macroeconomic scenarios by evaluating:
- **Fiscal Multipliers:** Balancing public spending cuts against short-term GDP impacts.
- **Strike Risk Index (0-100):** Captures socio-political friction where aggressive pension and public job cuts escalate social unrest, which can be mitigated by social buffers (hospital and student funding).
- **Auto-Solver:** Uses prescriptive optimisation (`itertools`) to systematically scan policy combinations that achieve the EU deficit limit (3%) without crossing critical unrest thresholds.
