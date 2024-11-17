from dash import html, dcc

def create_sidebar():
    return html.Div([
        # Search
        html.Div([
            dcc.Input(
                placeholder="Search instruments...",
                type="text",
                className="w-full px-4 py-2 bg-gray-800 text-gray-100 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500"
            )
        ], className="mb-6"),

        # Filters
        html.Div([
            html.H3("Filters", className="text-lg font-semibold text-gray-200 mb-4"),
            
            # Date Range
            html.Div([
                html.Label("Date Range", className="text-sm text-gray-400"),
                dcc.DatePickerRange(
                    id='date-range',
                    className="bg-gray-800"
                )
            ], className="mb-4"),
            
            # Sector Filter
            html.Div([
                html.Label("Sector", className="text-sm text-gray-400"),
                dcc.Dropdown(
                    id='sector-filter',
                    options=[
                        {'label': 'Financial', 'value': 'FIN'},
                        {'label': 'Technology', 'value': 'TECH'},
                        {'label': 'Energy', 'value': 'ENGY'},
                    ],
                    className="bg-gray-800 text-gray-200"
                )
            ], className="mb-4"),
            
            # Rating Filter
            html.Div([
                html.Label("Rating", className="text-sm text-gray-400"),
                dcc.Dropdown(
                    id='rating-filter',
                    options=[
                        {'label': 'AAA', 'value': 'AAA'},
                        {'label': 'AA', 'value': 'AA'},
                        {'label': 'A', 'value': 'A'},
                        {'label': 'BBB', 'value': 'BBB'},
                    ],
                    className="bg-gray-800 text-gray-200"
                )
            ], className="mb-4"),
            
            # Basis Threshold
            html.Div([
                html.Label("Basis Threshold (bps)", className="text-sm text-gray-400"),
                dcc.Input(
                    type="number",
                    value=50,
                    className="w-full px-4 py-2 bg-gray-800 text-gray-100 border border-gray-700 rounded-lg"
                )
            ], className="mb-4"),
        ], className="mb-6"),
        
        # Action Buttons
        html.Div([
            html.Button(
                "Apply Filters",
                className="w-full mb-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            ),
            html.Button(
                "Reset",
                className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
            ),
        ], className="mt-auto")
    ], className="w-64 bg-gray-900 p-6 border-r border-gray-700 h-full flex flex-col")
