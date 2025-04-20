import pandas as pd
from typing import List, Dict
import plotly.graph_objects as go
import numpy as np

def combine_asw_spreads(bonds: List[str], api_client) -> pd.DataFrame:
    # Dictionary to store individual dataframes
    all_spreads = {}
    
    # Loop through each bond and fetch its ASW spread
    for bond in bonds:
        try:
            # Get the DataFrame from the API
            df = api_client.get_asw_spread(bond)
            # Store the ASW spread column, using the bond name as the column name
            all_spreads[bond] = df['asw_spread']  # Adjust column name if different
        except Exception as e:
            print(f"Error fetching data for bond {bond}: {e}")
            continue
    
    # Combine all series into a single DataFrame
    # outer join to keep all dates from all bonds
    combined_df = pd.concat(all_spreads, axis=1)
    
    return combined_df

def create_spread_analysis_chart(df):
    # Get the last valid values for each metric
    current_values = df.apply(lambda col: col.dropna().iloc[-1] if pd.isna(col.iloc[-1]) else col.iloc[-1])
    
    # Calculate rolling statistics and get their last valid values
    rolling_mean = df.rolling(window=60).mean().apply(lambda col: col.dropna().iloc[-1] if pd.isna(col.iloc[-1]) else col.iloc[-1])
    rolling_std = df.rolling(window=60).std().apply(lambda col: col.dropna().iloc[-1] if pd.isna(col.iloc[-1]) else col.iloc[-1])
    
    # Create the figure
    fig = go.Figure()
    
    # Add error bars (2 standard deviations)
    fig.add_trace(go.Scatter(
        x=df.columns,
        y=rolling_mean,
        error_y=dict(
            type='data',
            array=rolling_std * 2,
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

# Example usage:
# Assuming your combined_df from the previous code
fig = create_spread_analysis_chart(result_df)
fig.show()
