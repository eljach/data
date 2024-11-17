from dash import html

def create_header():
    return html.Header(
        html.Div([
            html.H1("CDS Basis Trading Analytics", 
                    className="text-2xl font-bold text-gray-100"),
            html.Div([
                html.Button("Settings", 
                           className="px-4 py-2 text-sm text-gray-300 hover:text-white"),
                html.Button("Profile", 
                           className="px-4 py-2 text-sm text-gray-300 hover:text-white"),
            ], className="flex items-center space-x-4")
        ], className="flex justify-between items-center px-6 py-4")
    , className="bg-gray-800 border-b border-gray-700")
