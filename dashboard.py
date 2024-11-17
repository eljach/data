from dash import html, dcc, Input, Output, State, callback, ALL
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Sample data at module level
colombia_data = {
    'Bond': ['COLOM 28s', 'COLOM 33s', 'COLOM 35s', 'COLOM 45s', 'COLOM 51s', 'COLOM 67s'],
    'Live': [17, 17, 13, 9, 5, 8],
    'CoD': [-2, -1, 1, -5, -4, -2],
    'CoW': [-8, -10, -12, -9, -7, -11],
    'Z3m': [4.7, 1.8, 2.1, 1.6, 1.4, 1.2],
    'Z6m': [4.3, 1.4, 2.5, 1.8, 1.2, 1.1],
    'Z12m': [0.9, 0.8, 0.5, 1.2, 1.3, 1.5]
}

brazil_data = {
    'Bond': ['BRAZIL 29s', 'BRAZIL 34s', 'BRAZIL 37s', 'BRAZIL 47s', 'BRAZIL 50s', 'BRAZIL 55s'],
    'Live': [15, 14, 12, 8, 6, 5],
    'CoD': [-1, -2, 1, -3, -2, -1],
    'CoW': [-6, -8, -10, -7, -5, -4],
    'Z3m': [3.7, 1.6, 2.0, 1.4, 1.2, 1.0],
    'Z6m': [3.3, 1.2, 2.3, 1.6, 1.0, 0.9],
    'Z12m': [0.8, 0.7, 0.4, 1.0, 1.1, 0.8]
}

mexico_data = {
    'Bond': ['MEX 31s', 'MEX 34s', 'MEX 41s', 'MEX 47s', 'MEX 53s', 'MEX 61s'],
    'Live': [12, 14, 11, 8, 7, 6],
    'CoD': [-1, -2, 0, -2, -1, -1],
    'CoW': [-5, -7, -8, -6, -4, -3],
    'Z3m': [2.8, 1.9, 2.1, 1.5, 1.3, 1.1],
    'Z6m': [2.5, 1.7, 2.0, 1.4, 1.1, 0.9],
    'Z12m': [0.7, 0.9, 0.6, 0.8, 1.0, 0.7]
}

chile_data = {
    'Bond': ['CHILE 29s', 'CHILE 32s', 'CHILE 42s', 'CHILE 50s', 'CHILE 61s', 'CHILE 71s'],
    'Live': [10, 12, 9, 7, 6, 5],
    'CoD': [-1, -1, -2, -1, -1, 0],
    'CoW': [-4, -6, -5, -3, -2, -1],
    'Z3m': [1.9, 1.7, 1.5, 1.2, 1.0, 0.8],
    'Z6m': [1.8, 1.5, 1.3, 1.0, 0.8, 0.6],
    'Z12m': [0.6, 0.8, 0.7, 0.5, 0.4, 0.3]
}

peru_data = {
    'Bond': ['PERU 30s', 'PERU 35s', 'PERU 40s', 'PERU 50s', 'PERU 55s', 'PERU 68s'],
    'Live': [13, 15, 12, 9, 8, 7],
    'CoD': [-2, -1, -2, -1, -1, 0],
    'CoW': [-6, -8, -7, -5, -4, -3],
    'Z3m': [2.5, 2.1, 1.8, 1.4, 1.2, 1.0],
    'Z6m': [2.3, 1.9, 1.6, 1.2, 1.0, 0.8],
    'Z12m': [0.8, 1.0, 0.7, 0.6, 0.5, 0.4]
}

panama_data = {
    'Bond': ['PANAMA 30s', 'PANAMA 36s', 'PANAMA 45s', 'PANAMA 53s', 'PANAMA 63s', 'PANAMA 68s'],
    'Live': [16, 15, 11, 7, 6, 5],
    'CoD': [-2, -1, 0, -4, -2, -1],
    'CoW': [-7, -9, -11, -8, -6, -4],
    'Z3m': [4.2, 1.7, 2.2, 1.5, 1.3, 1.1],
    'Z6m': [3.8, 1.3, 2.4, 1.7, 1.5, 1.2],
    'Z12m': [0.9, 0.8, 0.6, 1.1, 0.9, 0.7]
}

domrep_data = {
    'Bond': ['DOMREP 29s', 'DOMREP 32s', 'DOMREP 41s', 'DOMREP 45s', 'DOMREP 55s', 'DOMREP 61s'],
    'Live': [18, 16, 13, 10, 8, 7],
    'CoD': [-3, -2, -1, -2, -1, -1],
    'CoW': [-9, -8, -6, -5, -4, -3],
    'Z3m': [3.2, 2.8, 2.1, 1.7, 1.4, 1.2],
    'Z6m': [2.9, 2.5, 1.9, 1.5, 1.2, 1.0],
    'Z12m': [1.1, 0.9, 0.7, 0.6, 0.5, 0.4]
}

def create_basis_chart(bond_name=None):
    # Generate dates for the last 30 days
    dates = [(datetime.now() - timedelta(days=x)).date() for x in range(30)]
    dates.reverse()

    # Generate data for the specific bond
    np.random.seed(42)  # For reproducibility
    base_pattern = np.cumsum(np.random.normal(0, 0.5, 30)) + np.linspace(0, 2, 30)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=base_pattern,
        name=bond_name,
        line=dict(color='#1f77b4', width=1.5),
        hovertemplate=
        '<b>%{x}</b><br>' +
        'Basis: %{y:.1f} bps<br>' +
        '<extra></extra>'
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Date",
        yaxis_title="Basis (bps)",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0.5)"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            tickformat='%Y-%m-%d'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=False
        ),
        hovermode='x unified'
    )
    
    return fig

def create_clickable_bond_name(bond_name, selected_bond=None):
    is_selected = bond_name == selected_bond
    return html.Div(
        bond_name, 
        className=f"w-40 font-medium text-xs cursor-pointer transition-colors duration-150 " + 
                 ("text-blue-400 bg-gray-800 rounded px-1" if is_selected else "text-gray-100 hover:text-blue-400"),
        id={'type': 'bond-name', 'bond': bond_name}
    )

def create_sovereign_basis_table(country, data, selected_bond=None):
    return html.Div([
        # Table Header
        html.Div([
            html.Div(country, className="text-lg font-bold text-white mb-3"),
            html.Div([
                html.Div("", className="w-40"),
                html.Div(
                    html.Div([
                        html.Div("Live", className="w-9 text-center"),
                        html.Div("CoD", className="w-9 text-center"),
                        html.Div("CoW", className="w-9 text-center"),
                        html.Div("σ3m", className="w-9 text-center"),
                        html.Div("σ6m", className="w-9 text-center"),
                        html.Div("σ12m", className="w-9 text-center"),
                    ], className="flex gap-[3px]")
                ),
            ], className="flex justify-between items-center text-gray-400 text-xs font-medium border-b border-gray-700 pb-2"),
        ]),
        
        # Table Body
        html.Div([
            *[html.Div([
                create_clickable_bond_name(data['Bond'][i], selected_bond),  # Pass selected_bond
                html.Div(
                    html.Div([
                        html.Div(f"{data['Live'][i]}", 
                                className="w-9 text-center text-sm font-medium"),
                        html.Div(f"{data['CoD'][i]:+d}", 
                                className=f"w-9 text-center text-sm {get_color_class(data['CoD'][i])}"),
                        html.Div(f"{data['CoW'][i]:+d}", 
                                className=f"w-9 text-center text-sm {get_color_class(data['CoW'][i])}"),
                        html.Div(f"{data['Z3m'][i]:.1f}", 
                                className=f"w-9 text-center text-sm {get_zscore_color_class(data['Z3m'][i])}"),
                        html.Div(f"{data['Z6m'][i]:.1f}", 
                                className=f"w-9 text-center text-sm {get_zscore_color_class(data['Z6m'][i])}"),
                        html.Div(f"{data['Z12m'][i]:.1f}", 
                                className=f"w-9 text-center text-sm {get_zscore_color_class(data['Z12m'][i])}"),
                    ], className="flex gap-[3px]")
                ),
            ], className="flex justify-between items-center py-1 hover:bg-gray-800")
            for i in range(len(data['Bond']))],
        ], className="text-gray-100"),
    ], className="bg-gray-900 p-4 rounded-lg")

def get_color_class(value):
    """Returns appropriate color class based on value"""
    if value > 0:
        return "text-green-500"
    elif value < 0:
        return "text-red-500"
    return "text-gray-100"

def get_zscore_color_class(value):
    """Returns appropriate color class based on z-score magnitude"""
    abs_value = abs(value)
    if abs_value > 2:
        return "text-red-500 font-medium"
    elif abs_value > 1:
        return "text-yellow-500 font-medium"
    return "text-gray-100"

def create_dashboard():
    return html.Div([
        # Main content wrapper with flex
        html.Div([
            # Store for selected bond
            dcc.Store(id='selected-bond', data=None),
            
            # Content container (tables and chart)
            html.Div([
                # Tables container
                html.Div([
                    # First row of tables
                    html.Div([
                        create_sovereign_basis_table("COLOM", colombia_data),
                        create_sovereign_basis_table("BRAZIL", brazil_data),
                        create_sovereign_basis_table("MEXICO", mexico_data),
                        create_sovereign_basis_table("CHILE", chile_data),
                    ], className="grid grid-cols-4 gap-4 mb-4", id='first-row-tables'),
                    
                    # Second row of tables
                    html.Div([
                        create_sovereign_basis_table("PERU", peru_data),
                        create_sovereign_basis_table("PANAMA", panama_data),
                        create_sovereign_basis_table("DOMREP", domrep_data),
                        html.Div(className="bg-transparent")
                    ], className="grid grid-cols-4 gap-4 mb-6", id='second-row-tables'),
                ], className="px-6"),
                
                # Hidden chart container
                html.Div([
                    html.Div([
                        html.H2(id="chart-title", className="text-xl font-bold text-white mb-4"),
                        dcc.Graph(
                            id='basis-chart',
                            className="h-96"
                        )
                    ], className="bg-gray-800 p-4 rounded-lg")
                ], className="px-6 mb-6", id="chart-container", style={'display': 'none'}),
            ], className="flex-grow"),
            
            # Footer - will stay at bottom
            html.Div([
                html.Span("Made with "),
                html.Span("❤️", className="text-red-500"),
                html.Span(" by Sebastian Eljach")
            ], className="text-center text-gray-400 text-xs py-3 border-t border-gray-800")
            
        ], className="flex flex-col min-h-screen"),
        
    ], className="flex-1 overflow-y-auto")

# Updated callbacks
@callback(
    Output("chart-container", "style"),
    Output("chart-title", "children"),
    Output("basis-chart", "figure"),
    Output("selected-bond", "data"),
    Output('first-row-tables', 'children'),
    Output('second-row-tables', 'children'),
    Input({"type": "bond-name", "bond": ALL}, "n_clicks"),
    State({"type": "bond-name", "bond": ALL}, "children"),
    State("selected-bond", "data"),
    prevent_initial_call=True
)
def update_chart(n_clicks, bond_names, current_selected):
    if not any(n_clicks):
        raise PreventUpdate
        
    # Find which bond was clicked
    clicked_idx = next(i for i, clicks in enumerate(n_clicks) if clicks)
    bond_name = bond_names[clicked_idx]
    
    # Create chart for selected bond
    fig = create_basis_chart(bond_name)
    
    # Recreate tables with new selected bond
    first_row = [
        create_sovereign_basis_table("COLOM", colombia_data, bond_name),
        create_sovereign_basis_table("BRAZIL", brazil_data, bond_name),
        create_sovereign_basis_table("MEXICO", mexico_data, bond_name),
        create_sovereign_basis_table("CHILE", chile_data, bond_name),
    ]
    
    second_row = [
        create_sovereign_basis_table("PERU", peru_data, bond_name),
        create_sovereign_basis_table("PANAMA", panama_data, bond_name),
        create_sovereign_basis_table("DOMREP", domrep_data, bond_name),
        html.Div(className="bg-transparent")
    ]
    
    return (
        {'display': 'block'},
        f"Historical Basis Evolution - {bond_name}",
        fig,
        bond_name,
        first_row,
        second_row
    )
