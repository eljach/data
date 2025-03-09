import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

class BondSpreadAnalyzer:
    def __init__(self, bloomberg_cache):
        self.bloomberg_cache = bloomberg_cache
        self.yields_df = None
        
    def get_bond_yields(self, bloomberg_client, bonds, start_date, end_date):
        """Fetch YTM data for multiple bonds"""
        yields_data = {}
        
        for bond in bonds:
            df = self.bloomberg_cache.get_timeseries(
                bloomberg_client,
                ticker=bond,
                fields=["YLD_YTM_BID"],
                start_date=start_date,
                end_date=end_date
            )
            yields_data[bond] = df["YLD_YTM_BID"]
        
        self.yields_df = pd.DataFrame(yields_data)
        return self.yields_df
    
    def calculate_zscore_matrix(self, window_days):
        """Calculate z-score matrix for all bond pairs using rolling window"""
        if self.yields_df is None:
            raise ValueError("No yield data available. Please run get_bond_yields first.")
            
        bonds = self.yields_df.columns
        n_bonds = len(bonds)
        zscore_matrix = pd.DataFrame(np.zeros((n_bonds, n_bonds)), 
                                   index=bonds, columns=bonds)
        
        for i, bond1 in enumerate(bonds):
            for j, bond2 in enumerate(bonds):
                if i != j:  # Skip diagonal
                    # Calculate spread
                    spread = self.yields_df[bond1] - self.yields_df[bond2]
                    
                    # Calculate rolling statistics
                    rolling_mean = spread.rolling(window=window_days).mean()
                    rolling_std = spread.rolling(window=window_days).std()
                    
                    # Calculate z-score using most recent values
                    current_spread = spread.iloc[-1]
                    current_mean = rolling_mean.iloc[-1]
                    current_std = rolling_std.iloc[-1]
                    
                    zscore = (current_spread - current_mean) / current_std
                    zscore_matrix.loc[bond1, bond2] = zscore
        
        return zscore_matrix
    
    def create_interactive_heatmap(self):
        """Create interactive heatmap with dropdown menu using Plotly"""
        # Define window options
        window_options = {
            '1 Month': 30,
            '2 Months': 60,
            '3 Months': 90,
            '6 Months': 180,
            '12 Months': 360
        }
        
        # Create figures for each window
        figures = []
        for window_name, window_days in window_options.items():
            zscore_matrix = self.calculate_zscore_matrix(window_days)
            
            fig = go.Heatmap(
                z=zscore_matrix.values,
                x=zscore_matrix.columns,
                y=zscore_matrix.index,
                text=np.round(zscore_matrix.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False,
                colorscale='RdBu',
                zmid=0,
                visible=False,
                name=window_name
            )
            figures.append(fig)
        
        # Make first figure visible
        figures[0].visible = True
        
        # Create figure with dropdown menu
        fig = go.Figure(data=figures)
        
        # Create dropdown menu
        updatemenus = [
            dict(
                buttons=list([
                    dict(
                        args=[{"visible": [i == j for j in range(len(figures))]}],
                        label=window_name,
                        method="update"
                    ) for i, window_name in enumerate(window_options.keys())
                ]),
                direction="down",
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
        
        # Update layout
        fig.update_layout(
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
                dict(text="Select Window:", x=0, y=1.12, yref="paper", xref="paper", showarrow=False)
            ]
        )
        
        return fig
