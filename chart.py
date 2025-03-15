def create_interactive_heatmap(self):
    """Create interactive heatmap with dropdown menu using Plotly"""
    # Define window options
    window_options = {
        '1 Month': 21,  # Approximately 21 trading days
        '2 Months': 42,
        '3 Months': 63,
        '6 Months': 126,
        '12 Months': 252
    }
    
    # Create base figure
    base_fig = go.Figure()
    
    # Store annotations for each window
    all_annotations = []
    
    # Create figures for each window
    for window_name, window_days in window_options.items():
        zscore_matrix = self.calculate_zscore_matrix(window_days)
        
        # Round values for display
        z_values = np.round(zscore_matrix.values, 2)
        
        # Create text matrix with empty strings for NaN values
        text = [[f'{x:.2f}' if not np.isnan(x) else '' for x in row] for row in z_values]
        
        # Create annotated heatmap
        fig = ff.create_annotated_heatmap(
            z=z_values,
            x=list(zscore_matrix.columns),
            y=list(zscore_matrix.index),
            annotation_text=text,
            colorscale='RdBu',
            zmid=0,
            zmin=-3,
            zmax=3,
            showscale=True,
            hoverongaps=False,
            font_colors=['black', 'black']
        )
        
        # Store this window's annotations
        window_annotations = list(fig.layout.annotations)
        all_annotations.append(window_annotations)
        
        # Add the heatmap trace
        for trace in fig.data:
            trace.visible = False  # Hide all traces initially
            base_fig.add_trace(trace)
    
    # Make first window visible
    for i in range(len(fig.data)):
        base_fig.data[i].visible = True
    
    # Create dropdown menu with buttons that update both traces and annotations
    buttons = []
    for idx, window_name in enumerate(window_options.keys()):
        # Calculate visibility list for traces
        visible = [i//len(fig.data) == idx for i in range(len(base_fig.data))]
        
        button = dict(
            args=[
                {'visible': visible},
                {'annotations': [
                    dict(text="Select Window:", x=0, y=1.12, yref="paper", xref="paper", 
                         showarrow=False, font=dict(size=14))
                ] + all_annotations[idx]}
            ],
            label=window_name,
            method='update'
        )
        buttons.append(button)
    
    # Update layout
    base_fig.update_layout(
        updatemenus=[{
            'buttons': buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }],
        title={
            'text': "Bond Yield Spread Z-Scores",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='versus Bond →',
        yaxis_title='Bond ↓',
        width=900,
        height=700,
        xaxis={'side': 'top'},
        yaxis={'autorange': 'reversed'},
        annotations=[
            dict(text="Select Window:", x=0, y=1.12, yref="paper", xref="paper", 
                 showarrow=False, font=dict(size=14))
        ] + all_annotations[0],  # Add first window's annotations
        margin=dict(t=150, l=100, r=50, b=50)
    )
    
    return base_fig
