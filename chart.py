import numpy as np
import pandas as pd
from datetime import datetime as dt
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

# 1. Input TES and IRS data
valuation_date = dt(2025, 4, 16)
bonds_data = pd.DataFrame([
    {"mty": dt(2026, 8, 26), "yield": 9.148, "irs_rate": 8.4121},
    {"mty": dt(2027, 11, 3), "yield": 9.611, "irs_rate": 7.9838},
    {"mty": dt(2028, 4, 28), "yield": 10.081, "irs_rate": 8.0357},
    {"mty": dt(2029, 8, 22), "yield": 10.870, "irs_rate": 8.2326},
    {"mty": dt(2030, 9, 18), "yield": 11.070, "irs_rate": 8.3898},
    {"mty": dt(2032, 6, 30), "yield": 11.821, "irs_rate": 8.658},
    {"mty": dt(2033, 2, 9), "yield": 12.070, "irs_rate": 8.7476},
    {"mty": dt(2034, 10, 18), "yield": 12.269, "irs_rate": 8.9605},
    {"mty": dt(2036, 7, 9), "yield": 12.540, "irs_rate": 9.1017},
    {"mty": dt(2040, 11, 28), "yield": 12.870, "irs_rate": 9.219},
    {"mty": dt(2042, 5, 28), "yield": 12.820, "irs_rate": 9.2361},
    {"mty": dt(2046, 7, 25), "yield": 13.030, "irs_rate": 9.2702},
    {"mty": dt(2050, 10, 26), "yield": 12.949, "irs_rate": 9.291},
])
bonds_data["ttm"] = bonds_data["mty"].apply(lambda x: (x - valuation_date).days / 365)
bonds_data["spread"] = bonds_data["yield"] - bonds_data["irs_rate"]

# 2. LOESS smoothing
loess_result = lowess(bonds_data["spread"], bonds_data["ttm"], frac=0.3, return_sorted=True)
ttm_smooth = loess_result[:, 0]
spread_smooth = loess_result[:, 1]

# 3. Penalized spline fit
penalized_spline = UnivariateSpline(ttm_smooth, spread_smooth, s=0.05)

# 4. Plot full curve with markers at annual tenors
ttm_grid = np.linspace(min(ttm_smooth), max(ttm_smooth), 300)
spread_fit = penalized_spline(ttm_grid)

# Evaluate at standard tenors for markers
standard_tenors = np.arange(1, 26, 1)
spread_markers = penalized_spline(standard_tenors)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(bonds_data["ttm"], bonds_data["spread"], 'o', label="Observed Spreads")
plt.plot(ttm_grid, spread_fit, '-', label="Penalized Spline Fit (P-spline)", linewidth=2)
plt.plot(standard_tenors, spread_markers, 's', label="Annual Tenor Markers", color='red')
plt.title("TES vs IRS Spread – Penalized Spline with Annual Markers")
plt.xlabel("Time to Maturity (Years)")
plt.ylabel("Spread (%)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
