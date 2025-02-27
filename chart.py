import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_mids_with_dispersion(results_df):
    """
    Create a plotly figure with two subplots:
    1. Line chart of average mids with highest/lowest range
    2. Bar chart showing mid dispersion
    
    Parameters:
    results_df (pd.DataFrame): DataFrame with columns [average_mid, highest_mid, lowest_mid, mid_spread]
    
    Returns:
    go.Figure: Plotly figure object
    """
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],  # 70% for mids, 30% for dispersion
        vertical_spacing=0.1,     # Space between subplots
        shared_xaxes=True        # Share x-axis (datetime)
    )
    
    # Add mid price line with markers
    fig.add_trace(
        go.Scatter(
            x=results_df.index,
            y=results_df['average_mid'],
            mode='lines+markers',
            name='Average Mid',
            line=dict(color='blue'),
            showlegend=True
        ),
        row=1, col=1
    )
    
    # Add highest/lowest range as a shaded area
    fig.add_trace(
        go.Scatter(
            x=results_df.index,
            y=results_df['highest_mid'],
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=results_df.index,
            y=results_df['lowest_mid'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(0, 0, 255, 0.1)',
            name='Price Range',
            showlegend=True
        ),
        row=1, col=1
    )
    
    # Add dispersion bars
    fig.add_trace(
        go.Bar(
            x=results_df.index,
            y=results_df['mid_spread'],
            name='Mid Dispersion',
            marker_color='rgb(158,202,225)',
            opacity=0.6
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title='Mid Prices and Dispersion Over Time',
        height=800,  # Increase overall height
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Update y-axes labels
    fig.update_yaxes(title_text="Mid Price", row=1, col=1)
    fig.update_yaxes(title_text="Dispersion", row=2, col=1)
    
    # Update x-axis
    fig.update_xaxes(title_text="Date", row=2, col=1)
    
    return fig

# Example usage:
"""
# Assuming your results dataframe is called 'results_df'
fig = plot_mids_with_dispersion(results_df)
fig.show()

# To save the plot as HTML:
# fig.write_html("mids_dispersion.html")
"""
