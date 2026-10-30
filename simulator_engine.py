import numpy as np
import pandas as pd

class FrancePolicyEngine:
    def __init__(self, gdp=2800, debt=112.5, median_wage=24500, tax_rate=0.45):
        self.gdp = gdp                      # Billions €
        self.debt = debt                    # Percentage of GDP (~112%)
        self.median_wage = median_wage      # Baseline gross wage
        self.tax_rate = tax_rate            # Effective tax burden

    def simulate_reforms(self, industrial_reshoring_boost, tax_cut_corp, labor_tax_shift, structural_pension_age):
        """
        Simulates prescriptive interventions:
        - Bringing back industries (Industrial Reshoring) -> Direct GDP booster
        - Smicardization & Middle-class squeeze -> Payroll tax adjustments
        - Debt & Taxation -> Fiscal management
        - Brain drain & Social stability -> Talent retention and risk index
        """
        
        # 1. Industrial Reshoring & Manufacturing Multiplier (Boosting GDP)
        # Bringing back industries increases domestic production, high-value exports, and local jobs.
        industrial_gdp_multiplier = industrial_reshoring_boost * 0.018 # Each slider tick adds a strong manufacturing GDP lift
        
        # 2. Combating Smicardization & Middle-Class Squeeze
        wage_growth_boost = (labor_tax_shift * 0.035) + (industrial_reshoring_boost * 0.01) 
        adjusted_median_wage = self.median_wage * (1 + wage_growth_boost)

        # 3. Overall GDP Growth Rate Calculation
        baseline_growth = 0.012 # 1.2% baseline
        gdp_growth_rate = baseline_growth + industrial_gdp_multiplier - (0.005 if tax_cut_corp > 0.08 else 0)
        new_gdp = self.gdp * (1 + gdp_growth_rate)
        
        # 4. Pension System Sustainability Index (0 to 100)
        pension_health = min(100, 60 + (structural_pension_age - 62) * 12 + (gdp_growth_rate * 200))

        # 5. Social Stability & Strike Risk Score (0 to 100, lower is better)
        inequality_penalty = max(0, (self.median_wage - adjusted_median_wage) / 1000)
        strike_risk_score = min(100, max(5, 40 + inequality_penalty - (industrial_reshoring_boost * 5) - (pension_health * 0.2)))

        # 6. Debt-to-GDP adjustment (Growing GDP naturally lowers the debt-to-GDP burden)
        new_debt_ratio = max(80.0, self.debt - (gdp_growth_rate * 35) + (tax_cut_corp * 10))

        return {
            "Projected GDP (€B)": round(new_gdp, 2),
            "GDP Growth Rate (%)": round(gdp_growth_rate * 100, 2),
            "New Debt-to-GDP (%)": round(new_debt_ratio, 2),
            "Adjusted Median Wage (€)": round(adjusted_median_wage, 2),
            "Pension System Sustainability Index": round(pension_health, 1),
            "Social Strike Risk Score (0-100)": round(strike_risk_score, 1)
        }
