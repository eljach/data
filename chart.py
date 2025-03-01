def plot_yields_with_spread(dates, series1, series2, spread, series1_name='5Y', series2_name='10Y'):
    """
    Create a plotly figure with two subplots:
    1. Dual-axis line chart of two yield series
    2. Line chart showing spread between yields
    
    Parameters:
    dates (pd.DatetimeIndex): Common dates for all series
    series1 (pd.Series): First yield series
    series2 (pd.Series): Second yield series
    spread (pd.Series): Spread between yields
    series1_name (str): Name for first series
    series2_name (str): Name for second series
    
    Returns:
    go.Figure: Plotly figure object
    """
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.1,
        shared_xaxes=True,
        specs=[[{"secondary_y": True}],
               [{"secondary_y": False}]]
    )
    
    # Add first yield series on primary y-axis
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=series1,
            mode='lines+markers',
            name=series1_name,
            line=dict(color='blue'),
            showlegend=True
        ),
        row=1, col=1,
        secondary_y=False
    )
    
    # Add second yield series on secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=series2,
            mode='lines+markers',
            name=series2_name,
            line=dict(color='red'),
            showlegend=True
        ),
        row=1, col=1,
        secondary_y=True
    )
    
    # Add spread as a line chart
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=spread,
            mode='lines+markers',
            name='Spread',
            line=dict(color='green'),
            showlegend=True
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f'{series1_name} vs {series2_name} Yields and Spread',
        height=800,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Update y-axes labels
    fig.update_yaxes(
        title_text=f"{series1_name} Yield",
        color="blue",
        row=1,
        col=1,
        secondary_y=False
    )
    fig.update_yaxes(
        title_text=f"{series2_name} Yield",
        color="red",
        row=1,
        col=1,
        secondary_y=True
    )
    fig.update_yaxes(
        title_text="Spread (bps)",
        color="green",
        row=2,
        col=1
    )
    
    # Update x-axis
    fig.update_xaxes(title_text="Date", row=2, col=1)
    
    return fig
