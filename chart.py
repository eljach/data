import pandas as pd
import plotly.graph_objects as go

# Assume daily_cumulative is already computed as before
# Columns: ['Date', 'Instrument', 'Cumulative_DV01']

# Create a line for each instrument manually
fig = go.Figure()

for instrument in daily_cumulative['Instrument'].unique():
    data = daily_cumulative[daily_cumulative['Instrument'] == instrument]
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Cumulative_DV01'],
        mode='lines+markers',  # 👈 this adds markers to the line
        name=instrument
    ))

fig.update_layout(
    title='Cumulative DV01 Exposure Over Time by Instrument',
    xaxis_title='Date',
    yaxis_title='Cumulative DV01',
    hovermode='x unified'
)

fig.show()
