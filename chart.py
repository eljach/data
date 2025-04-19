import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------
# 1.  Load / prepare the raw time‑series
# ----------------------------------------
# Assume you have a DataFrame or Series called `spreads`
#   • Index: datetime64[ns] ‑‑ one row per trading day
#   • Column (or Series name): 'spread'  (in bp)

# Example placeholder (delete when you plug in your data):
# spreads = (
#     pd.Series(
#         data=np.random.normal(loc=10, scale=15, size=520),
#         index=pd.bdate_range("2005‑01‑03", periods=520, freq="B"),
#         name="spread"
#     )
#     .to_frame()
# )

df = spreads.copy()

# ----------------------------------------
# 2.  Three‑month rolling statistics
# ----------------------------------------
ROLL_DAYS = 63        # 63 business days ≈ 3 calendar months
df["roll_mean_3m"] = df["spread"].rolling(ROLL_DAYS).mean()
df["roll_std_3m"]  = df["spread"].rolling(ROLL_DAYS).std()

# ----------------------------------------
# 3.  Pick the “snapshot” dates you want on the x‑axis
#     (here: last business‑day of every third month)
# ----------------------------------------
snapshots = (
    df.resample("3M")        # every three calendar months
      .last()                # last obs. in that window
      .dropna(subset=["roll_mean_3m"])   # need full window
)

# ----------------------------------------
# 4.  Build the Plotly figure
# ----------------------------------------
fig = go.Figure()

# ‑‑ 3‑month average with ±2σ error bars
fig.add_trace(
    go.Scatter(
        x=snapshots.index,
        y=snapshots["roll_mean_3m"],
        mode="markers",
        marker_symbol="circle",
        name="3‑month avg",
        error_y=dict(
            type="data",
            array=2 * snapshots["roll_std_3m"],   # ±2σ
            symmetric=True,
            thickness=3
        ),
    )
)

# ‑‑ Spot value
fig.add_trace(
    go.Scatter(
        x=snapshots.index,
        y=snapshots["spread"],
        mode="markers",
        marker_symbol="x",
        name="Spot"
    )
)

fig.update_layout(
    title="Asset‑swap spreads — spot vs 3‑month average and 2σ bands",
    xaxis_title="Date",
    yaxis_title="Spread (bp)",
    template="simple_white",
    showlegend=True
)

fig.show()
