import plotly.figure_factory as ff

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
    
    # Create figures for each window
    figures = []
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
            font_colors=['black', 'black']  # Use black text for all cells
        )
        
        # Ensure annotations are visible and properly formatted
        for annotation in fig.layout.annotations:
            annotation.update(
                font=dict(
                    size=12,
                    color='black'
                ),
                showarrow=False
            )
        
        # Update traces
        fig.update_traces(
            visible=False,
            hovertemplate=(
                "Row Bond: %{y}<br>" +
                "Column Bond: %{x}<br>" +
                "Z-score: %{z:.2f}<br>" +
                "<extra></extra>"
            )
        )
        
        figures.append(fig)
    
    # Create base figure
    base_fig = go.Figure()
    
    # Add all traces from all figures
    for fig in figures:
        for trace in fig.data:
            base_fig.add_trace(trace)
        # Add annotations from each figure
        if len(figures) == 1:
            base_fig.layout.annotations = fig.layout.annotations
        else:
            # For multiple figures, we need to handle annotations differently
            annotations_per_fig = len(fig.layout.annotations)
            for ann in fig.layout.annotations:
                base_fig.add_annotation(ann)
    
    # Make first figure's traces visible
    num_traces_per_fig = len(figures[0].data)
    for i in range(num_traces_per_fig):
        base_fig.data[i].visible = True
    
    # Create dropdown menu
    updatemenus = [
        dict(
            buttons=[
                dict(
                    args=[{
                        'visible': [True if i//num_traces_per_fig == j else False 
                                  for i in range(len(base_fig.data))]
                    }],
                    label=window_name,
                    method="update"
                ) for j, window_name in enumerate(window_options.keys())
            ],
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )
    ]
    
    # Update layout
    base_fig.update_layout(
        updatemenus=updatemenus,
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
            dict(
                text="Select Window:",
                x=0,
                y=1.12,
                yref="paper",
                xref="paper",
                showarrow=False,
                font=dict(size=14)
            ),
            *base_fig.layout.annotations  # Add the heatmap annotations
        ],
        margin=dict(t=150, l=100, r=50, b=50)
    )
    
    return base_fig
