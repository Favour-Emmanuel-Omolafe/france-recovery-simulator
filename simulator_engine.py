import pandas as pd


def run_macro_simulation(**kwargs):
  """Executes the complete macroeconomic simulation based on user-defined

  policy levers, global shocks, and social buffers. Computes debt paths,
  GDP growth, and dynamic civil unrest risk.
  """
  # Extract input parameters from Streamlit sliders
  ecb_rate = kwargs.get("ecb_rate", 3.2)
  energy_shock = kwargs.get("energy_shock", "Moderate")
  retirement_age = kwargs.get("retirement_age", 64)
  wealth_tax_isf = kwargs.get("wealth_tax_isf", False)
  industrial_reshoring = kwargs.get("industrial_reshoring", 3.0)
  talent_retention = kwargs.get("talent_retention", 1.5)
  admin_savings = kwargs.get("admin_savings", 5.0)
  public_job_cuts = kwargs.get("public_job_cuts", 2.0)
  corporate_tax_adj = kwargs.get("corporate_tax_adj", 0.0)
  hospital_funding = kwargs.get("hospital_funding", 3.0)
  youth_grants = kwargs.get("youth_grants", 1.5)

  # ---------------------------------------------------------
  # 1. DYNAMIC CIVIL UNREST & SOCIAL FRICTION MODELING
  # ---------------------------------------------------------
  # Realistic French political friction: Raising retirement age past 64 heavily drives unrest
  retirement_penalty = max(0, retirement_age - 64) * 8.0

  # Energy shock penalty
  energy_shock_val = (
      3.5 if energy_shock == "Severe" else (2.0 if energy_shock == "Moderate" else 0.0)
  )

  # Calculate total social friction score with balanced weights
  unrest_score = (
      (public_job_cuts * 2.5)
      + retirement_penalty
      + energy_shock_val
      + (max(0, ecb_rate - 3.5) * 1.5)
      - (hospital_funding * 0.8)
      - (youth_grants * 0.8)
      - (1.5 if wealth_tax_isf else 0.0)
  )

  # Categorize risk index dynamically
  if unrest_score > 9:
    strike_risk = "🔴 High (General Strikes Likely)"
  elif unrest_score > 4:
    strike_risk = "🟡 Moderate (Sector Protests)"
  else:
    strike_risk = "🟢 Low (Socially Stable)"

  # ---------------------------------------------------------
  # 2. MACROECONOMIC & DEBT TRAJECTORY MODELING
  # ---------------------------------------------------------
  base_debt_2036 = 112.0
  fiscal_relief = (
      (admin_savings * 0.35)
      + (public_job_cuts * 0.45)
      + (max(0, retirement_age - 64) * 0.8)
      + (2.5 if wealth_tax_isf else 0.0)
  )
  investment_drain = (industrial_reshoring * 0.15) + (talent_retention * 0.1)
  macro_penalty = (ecb_rate * 0.25) + (energy_shock_val * 0.3)

  projected_debt = round(
      base_debt_2036 - fiscal_relief + investment_drain + macro_penalty, 1
  )

  # GDP growth calculation
  base_gdp = 1.2
  gdp_growth = round(
      base_gdp
      + (industrial_reshoring * 0.06)
      + (talent_retention * 0.08)
      - (abs(corporate_tax_adj) * 0.03),
      2,
  )

  # 10-Year Trajectory Dataframe for the chart
  years = list(range(2026, 2037))
  baseline_path = [110.0 + (i * 0.45) for i in range(len(years))]

  saving_factor = 0.3 if fiscal_relief > 8.0 else 0.15
  optimized_path = [
      max(95.0, 110.0 - (i * saving_factor) + (macro_penalty * 0.1))
      for i in range(len(years))
  ]

  trajectory_df = pd.DataFrame(
      {
          "Baseline Debt Path (%)": baseline_path,
          "Optimized Policy Path (%)": optimized_path,
      },
      index=years,
  )

  return {
      "debt_2036": projected_debt,
      "gdp_growth": gdp_growth,
      "strike_risk": strike_risk,
      "trajectory": trajectory_df,
  }
