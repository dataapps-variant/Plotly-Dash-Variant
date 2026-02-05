"""
Variant Analytics Dashboard - Main Entry Point
Plotly Dash Version

To run:
    python app/main.py

Environment Variables:
    GCS_CACHE_BUCKET - GCS bucket name for caching (optional)
    GOOGLE_APPLICATION_CREDENTIALS - Path to service account JSON
    SECRET_KEY - Flask secret key for sessions
"""

import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dash import Dash, html, dcc, Input, Output, State, callback, no_update, ALL, MATCH
from flask import session
import dash_bootstrap_components as dbc

from config import APP_NAME, DASHBOARDS, DEFAULT_BC, DEFAULT_COHORT, DEFAULT_PLAN, CHART_METRICS
from theme import get_base_stylesheet, get_theme_colors
from auth import authenticate, logout, is_authenticated, get_current_user, is_admin

# Initialize the Dash app with Flask server
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    ],
    title=APP_NAME
)

# Configure Flask server for sessions
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'variant-dashboard-secret-key-change-in-production')

# =============================================================================
# LAYOUT
# =============================================================================

app.layout = html.Div([
    # URL for routing
    dcc.Location(id='url', refresh=False),
    
    # Store for theme
    dcc.Store(id='theme-store', data='dark', storage_type='local'),
    
    # Store for authentication state
    dcc.Store(id='auth-store', data={'authenticated': False}),
    
    # Dynamic stylesheet
    html.Style(id='dynamic-styles'),
    
    # Main content container
    html.Div(id='page-content', style={'minHeight': '100vh'})
])


# =============================================================================
# THEME CALLBACK
# =============================================================================

@callback(
    Output('dynamic-styles', 'children'),
    Input('theme-store', 'data')
)
def update_styles(theme):
    """Update CSS based on theme"""
    return get_base_stylesheet(theme)


# =============================================================================
# ROUTING CALLBACK
# =============================================================================

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('theme-store', 'data')
)
def display_page(pathname, theme):
    """Route to appropriate page based on URL"""
    
    # Check authentication
    if not is_authenticated():
        from pages.login import create_login_layout
        return create_login_layout(theme)
    
    # Route based on pathname
    if pathname == '/' or pathname == '/landing':
        from pages.landing import create_landing_layout
        return create_landing_layout(theme)
    
    elif pathname == '/icarus_historical':
        from pages.icarus_historical import create_icarus_layout
        return create_icarus_layout(theme)
    
    elif pathname == '/admin':
        if is_admin():
            from pages.admin_panel import create_admin_layout
            return create_admin_layout(theme)
        else:
            from pages.landing import create_landing_layout
            return create_landing_layout(theme)
    
    elif pathname == '/logout':
        logout()
        from pages.login import create_login_layout
        return create_login_layout(theme)
    
    else:
        # Default to landing page
        from pages.landing import create_landing_layout
        return create_landing_layout(theme)


# =============================================================================
# LOGIN CALLBACK
# =============================================================================

@callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('login-error', 'children'),
     Output('login-error', 'style')],
    Input('login-btn', 'n_clicks'),
    [State('username-input', 'value'),
     State('password-input', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    """Handle login form submission"""
    if n_clicks is None:
        return no_update, no_update, no_update
    
    if not username or not password:
        return no_update, "Please enter both username and password", {'display': 'block', 'color': '#F87171'}
    
    if authenticate(username, password):
        return '/landing', "", {'display': 'none'}
    else:
        return no_update, "Invalid username or password", {'display': 'block', 'color': '#F87171'}


# =============================================================================
# THEME TOGGLE CALLBACK
# =============================================================================

@callback(
    Output('theme-store', 'data'),
    Input('theme-toggle-btn', 'n_clicks'),
    State('theme-store', 'data'),
    prevent_initial_call=True
)
def toggle_theme(n_clicks, current_theme):
    """Toggle between dark and light theme"""
    if n_clicks is None:
        return no_update
    return 'light' if current_theme == 'dark' else 'dark'


# =============================================================================
# NAVIGATION CALLBACKS
# =============================================================================

@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input({'type': 'nav-btn', 'page': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_page(n_clicks_list):
    """Navigate to selected dashboard page"""
    from dash import ctx
    
    if not any(n_clicks_list):
        return no_update
    
    triggered_id = ctx.triggered_id
    if triggered_id and isinstance(triggered_id, dict):
        return f"/{triggered_id['page']}"
    
    return no_update


@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('back-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_back(n_clicks):
    """Handle back button"""
    if n_clicks:
        return '/landing'
    return no_update


@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('logout-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """Handle logout button"""
    if n_clicks:
        logout()
        return '/logout'
    return no_update


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Get port from environment or default to 8050
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Variant Analytics Dashboard on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run_server(
        debug=debug,
        host='0.0.0.0',
        port=port
    )
