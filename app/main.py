"""
Variant Analytics Dashboard - Main Entry Point (Dash Version)
Version 2.0 - Complete Redesign

To run:
    python app/main.py

Environment Variables:
    GCS_CACHE_BUCKET - GCS bucket name for caching (optional)
    GOOGLE_APPLICATION_CREDENTIALS - Path to service account JSON
"""

import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import Dash, html, dcc, Input, Output, State, callback, no_update

from config import APP_NAME
from theme import generate_css, get_theme_colors
from auth import authenticate, is_admin

# Initialize Dash app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title=APP_NAME,
    update_title=None,
)

# Configure Flask session for authentication
app.server.secret_key = os.environ.get('SECRET_KEY', 'variant-dashboard-secret-key-change-in-production')

# =============================================================================
# APP LAYOUT
# =============================================================================

app.layout = html.Div([
    # URL routing
    dcc.Location(id='url', refresh=False),
    
    # Theme store
    dcc.Store(id='theme-store', storage_type='local', data='dark'),
    
    # User session store
    dcc.Store(id='user-store', storage_type='session', data=None),
    
    # Dynamic CSS
    html.Style(id='dynamic-css'),
    
    # Main content container
    html.Div(id='page-content', className='dash-container'),
    
], id='root')


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output('dynamic-css', 'children'),
    Input('theme-store', 'data')
)
def update_css(theme):
    """Update CSS based on theme"""
    return generate_css(theme or 'dark')


@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('user-store', 'data'), State('theme-store', 'data')]
)
def display_page(pathname, user, theme):
    """Route to appropriate page based on URL and auth state"""
    theme = theme or 'dark'
    colors = get_theme_colors(theme)
    
    try:
        from pages.login import create_login_layout
        from pages.landing import create_landing_layout
        from pages.icarus_historical import create_icarus_layout
        from pages.admin_panel import create_admin_layout
        
        # Not authenticated - show login
        if not user:
            return create_login_layout(theme)
        
        # Route based on pathname
        if pathname == '/admin':
            if is_admin(user):
                return create_admin_layout(user, theme)
            else:
                return create_landing_layout(user, theme)
        elif pathname == '/icarus_historical':
            return create_icarus_layout(user, theme)
        else:
            # Default to landing
            return create_landing_layout(user, theme)
    except Exception as e:
        # Return error page if something goes wrong
        return html.Div([
            html.H1('Error', style={'color': colors['danger']}),
            html.P(f'An error occurred: {str(e)}', style={'color': colors['text_primary']}),
            html.Pre(str(e), style={'color': colors['text_secondary'], 'whiteSpace': 'pre-wrap'}),
        ], style={'padding': '40px', 'textAlign': 'center'})


# Login callback
@callback(
    [Output('user-store', 'data'), Output('login-error', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'), State('password-input', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    """Handle login form submission"""
    if not n_clicks:
        return no_update, no_update
    
    if not username or not password:
        return None, html.Div("Please enter both username and password", className='alert alert-warning')
    
    user = authenticate(username, password)
    if user:
        return user, html.Div("Login successful!", className='alert alert-success')
    else:
        return None, html.Div("Invalid username or password", className='alert alert-danger')


# Logout callback
@callback(
    Output('user-store', 'data', allow_duplicate=True),
    [Input('logout-button', 'n_clicks')],
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """Handle logout"""
    if n_clicks:
        return None
    return no_update


# Theme toggle callback
@callback(
    Output('theme-store', 'data'),
    [Input('theme-toggle', 'n_clicks')],
    [State('theme-store', 'data')],
    prevent_initial_call=True
)
def toggle_theme(n_clicks, current_theme):
    """Toggle between dark and light theme"""
    if n_clicks:
        return 'light' if current_theme == 'dark' else 'dark'
    return current_theme


# =============================================================================
# RUN SERVER
# =============================================================================

# Get port from environment variable (Cloud Run sets PORT=8080)
port = int(os.environ.get('PORT', 8050))

# Expose server for gunicorn
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=port)
