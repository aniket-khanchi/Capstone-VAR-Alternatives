import pandas as pd
import numpy as np
import yfinance as yf

def var_historical_simulation(data, confidence_level, window):
  """
  Calculates Value at Risk (VAR) using historical simulation.

  Args:
      data (pd.DataFrame): DataFrame containing historical asset returns.
      confidence_level (float): Confidence level for VAR (e.g., 0.95).
      window (int): Window size for historical simulations (e.g., 252 for daily data).

  Returns:
      float: VAR value at the specified confidence level.
  """

  # Calculate daily percentage changes
  daily_returns = data.pct_change()

  # Simulate portfolio losses based on historical returns
  simulations = []
  for _ in range(window):
    # Randomly sample a historical return period
    daily_shock = daily_returns.sample(replace=True, window=window)
    # Calculate the one-day loss based on the simulated returns
    portfolio_loss = daily_shock.sum()
  
    simulations.append(portfolio_loss)

  # Sort the simulated losses from least to greatest
  simulations.sort()

  # Calculate the VAR value at the specified confidence level
  var_index = int(len(simulations) * confidence_level)
  var_value = simulations[var_index]

  return var_value

# Example usage
# Assuming you have a pandas DataFrame 'data' with historical daily returns
confidence_level = 0.95
window = 252  # Daily data for one year

data = yf.download("^IXIC", start="2020-01-01", end="2024-06-25")

var = var_historical_simulation(data, confidence_level, window)

print(f"VAR at {confidence_level*100:.0f}% confidence level: {var:.2f}")
