import numpy as np
import pandas as pd

class FrancePolicyEngine:
    def __init__(self, gdp=2800, debt=112.5, median_wage=24500, tax_rate=0.45):
        self.gdp = gdp                      # Billions €
        self.debt = debt                    # Percentage of GDP (~112%)
        self.median_wage = median_wage      # Annual gross SMIC/mid-bracket baseline
        self.tax_rate = tax_rate            # Effective tax burden

    def simulate_reforms(self, tax_cut_corp, rd_subsidy, labor_tax_shift, structural_pension_age):
        """
        Simulates prescriptive interventions addressing deindustrialization, 
        smicardization, brain drain, and debt sustainability.
        """
        # 1. Combating Smicardization & Middle-Class Squeeze
        wage_growth_boost = labor_tax_shift * 0.035 
        adjusted_median_wage = self.median_wage * (1 + wage_growth_boost)

        # 2. Laffer Curve & Corporate Tax Impact on Deindustrialization
        tax_elasticity = 0.4 
        effective_tax = max(0.15, self.tax_rate - tax_cut_corp)
        industrial_capex_growth = tax_cut_corp * tax_elasticity

        # 3. Brain Drain & R&D Multiplier
        rd_impact = rd_subsidy * 0.025 
        
        # 4. GDP Growth & Debt Dynamics
        baseline_growth = 0.012 
        gdp_growth_rate = baseline_growth + (industrial_capex_growth * 0.015) + rd_impact - (0.005 if tax_cut_corp > 0.08 else 0)
        new_gdp = self.gdp * (1 + gdp_growth_rate)
        
        # 5. Pension System Sustainability Index (0 to 100)
        pension_health = min(100, 60 + (structural_pension_age - 62) * 12 + (gdp_growth_rate * 200))

        # 6. Social Stability & Strike Risk Score (0 to 100, lower is better)
        inequality_penalty = max(0, (self.median_wage - adjusted_median_wage) / 1000)
        tax_friction_penalty = max(0, (effective_tax - 0.4) * 50)
        strike_risk_score = min(100, max(5, 40 + inequality_penalty + tax_friction_penalty - (pension_health * 0.2)))

        new_debt_ratio = max(80.0, self.debt - (gdp_growth_rate * 30) + (tax_cut_corp * 10))

        return {
            "Projected GDP (€B)": round(new_gdp, 2),
            "GDP Growth Rate (%)": round(gdp_growth_rate * 100, 2),
            "New Debt-to-GDP (%)": round(new_debt_ratio, 2),
            "Adjusted Median Wage (€)": round(adjusted_median_wage, 2),
            "Pension System Sustainability Index": round(pension_health, 1),
            "Social Strike Risk Score (0-100)": round(strike_risk_score, 1)
        }
