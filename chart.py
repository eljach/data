import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ipywidgets import interact, Dropdown
import plotly.express as px

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
        """
        Calculate z-score matrix for all bond pairs using rolling window
        
        Parameters:
        -----------
        window_days : int
            Number of days for rolling window
            
        Returns:
        --------
        pandas.DataFrame : Matrix of z-scores
        """
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
    
    def plot_zscore_heatmap(self):
        """Create interactive heatmap with time window selection"""
        
        def update_heatmap(window):
            # Convert window selection to days
            window_days = {
                '1 Month': 30,
                '2 Months': 60,
                '3 Months': 90,
                '6 Months': 180,
                '12 Months': 360
            }[window]
            
            # Calculate z-score matrix
            zscore_matrix = self.calculate_zscore_matrix(window_days)
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=zscore_matrix.values,
                x=zscore_matrix.columns,
                y=zscore_matrix.index,
                text=np.round(zscore_matrix.values, 2),
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False,
                colorscale='RdBu',  # Red-White-Blue colorscale
                zmid=0,  # Center the colorscale at 0
                colorbar=dict(
                    title='Z-Score',
                    titleside='right'
                )
            ))
            
            fig.update_layout(
                title=f'Bond Yield Spread Z-Scores ({window} Rolling Window)',
                xaxis_title='versus Bond →',
                yaxis_title='Bond ↓',
                width=900,
                height=700,
                xaxis={'side': 'top'},  # Move x-axis labels to top
                yaxis={'autorange': 'reversed'}  # Reverse y-axis to match matrix format
            )
            
            return fig
        
        # Create dropdown widget
        window_options = ['1 Month', '2 Months', '3 Months', '6 Months', '12 Months']
        
        interact(
            update_heatmap,
            window=Dropdown(
                options=window_options,
                value='1 Month',
                description='Window:',
                style={'description_width': 'initial'}
            )
        )
