```python
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------
# 1.  INPUT  ── df_raw: wide DataFrame with ASW time‑series
# -----------------------------------------------------------------
#   • Index: datetime64[ns] (daily or business‑day observations)
#   • Columns: one column per bond (ASW spread in bp)
# -----------------------------------------------------------------
# df_raw = pd.read_csv("asw_levels.csv", index_col=0, parse_dates=True)

ROLL_DAYS = 63   # ≈ 3 calendar months of business days

# ── tidy & chronologically sorted copy
_df = df_raw.sort_index()

# -----------------------------------------------------------------
# 2.  Three‑month rolling statistics (per bond)
# -----------------------------------------------------------------
roll_mean = _df.rolling(ROLL_DAYS, min_periods=ROLL_DAYS).mean()
roll_std  = _df.rolling(ROLL_DAYS, min_periods=ROLL_DAYS).std()

# -----------------------------------------------------------------
# 3.  Extract **latest** measurements for each bond
# -----------------------------------------------------------------
spot      = _df.iloc[-1]         # last available value (series)
mean_3m   = roll_mean.iloc[-1]   # last 3‑m rolling mean
std_3m    = roll_std.iloc[-1]    # last 3‑m rolling std

# Keep only bonds that have a full 3‑month window (no NaNs)
mask      = mean_3m.notna() & std_3m.notna()
bonds     = mean_3m.index[mask]

spot      = spot[bonds]
mean_3m   = mean_3m[bonds]
std_3m    = std_3m[bonds]

# -----------------------------------------------------------------
# 4.  Build *one* Plotly figure: x‑axis = bonds (categorical)
# -----------------------------------------------------------------
fig = go.Figure()

# ── 3‑month average + error bars (±2σ)
fig.add_trace(
    go.Scatter(
        x=bonds,
        y=mean_3m,
        mode="markers",
        name="3‑month avg",
        marker_symbol="circle",
        marker_size=10,
        error_y=dict(
            type="data",
            array=2 * std_3m,      # ±2σ
            symmetric=True,
            thickness=3,
            color="red"
        ),
    )
)

# ── Spot (latest) spread level
fig.add_trace(
    go.Scatter(
        x=bonds,
        y=spot,
        mode="markers",
        name="Spot value",
        marker_symbol="x",
        marker_size=12,
    )
)

fig.update_layout(
    title="Asset‑swap spreads — Spot vs 3‑month average ± 2σ",
    xaxis_title="Bond / Maturity",
    yaxis_title="Spread (bp)",
    template="simple_white",
    showlegend=True,
    legend=dict(x=0.01, y=0.99)
)

fig.show()
```
