import plotly.graph_objects as go
import numpy as np
import pandas as pd

def create_spread_analysis_chart(df):
    current_values = []
    rolling_means = []
    rolling_stds = []
    
    # Process each bond independently
    for bond in df.columns:
        # Get clean series for this bond
        clean_series = df[bond].dropna()
        
        if not clean_series.empty:
            # Calculate statistics for clean data
            current_values.append(clean_series.iloc[-1])
            rolling_mean = clean_series.rolling(window=60).mean().iloc[-1]
            rolling_std = clean_series.rolling(window=60).std().iloc[-1]
            rolling_means.append(rolling_mean)
            rolling_stds.append(rolling_std)
        else:
            # Handle empty series
            current_values.append(np.nan)
            rolling_means.append(np.nan)
            rolling_stds.append(np.nan)
    
    # Create the figure
    fig = go.Figure()
    
    # Add error bars (2 standard deviations)
    fig.add_trace(go.Scatter(
        x=df.columns,
        y=rolling_means,
        error_y=dict(
            type='data',
            array=[std * 2 for std in rolling_stds],
            color='red',
            thickness=1.5,
            width=10
        ),
        mode='markers',
        marker=dict(
            color='blue',
            size=10,
            symbol='circle'
        ),
        name='3-month Average'
    ))
    
    # Add current values
    fig.add_trace(go.Scatter(
        x=df.columns,
        y=current_values,
        mode='markers',
        marker=dict(
            color='black',
            size=10,
            symbol='circle'
        ),
        name='Current Value'
    ))
    
    # Update layout
    fig.update_layout(
        title='Asset Swap Spreads Analysis',
        yaxis_title='Spread (bps)',
        xaxis_title='Bonds',
        showlegend=True,
        template='plotly_white',
        yaxis=dict(zeroline=True),
        height=600,
        width=800
    )
    
    return fig
