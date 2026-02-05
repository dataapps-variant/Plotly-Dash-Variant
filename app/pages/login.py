"""
Login Page for Variant Analytics Dashboard - Plotly Dash Version
"""

from dash import html, dcc
from theme import get_theme_colors


def create_login_layout(theme="dark"):
    """Create the login page layout"""
    
    colors = get_theme_colors(theme)
    
    return html.Div([
        # Theme toggle in corner
        html.Div([
            html.Button(
                "☀️" if theme == "dark" else "🌙",
                id='theme-toggle-btn',
                style={
                    'background': 'transparent',
                    'border': f'1px solid {colors["border"]}',
                    'borderRadius': '8px',
                    'padding': '8px 12px',
                    'cursor': 'pointer',
                    'color': colors['text_primary']
                }
            )
        ], style={
            'position': 'absolute',
            'top': '20px',
            'right': '20px'
        }),
        
        # Logo and header
        html.Div([
            # Logo placeholder (V in a box)
            html.Div([
                html.Div("V", style={
                    'width': '80px',
                    'height': '80px',
                    'background': colors['accent'],
                    'borderRadius': '12px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'fontSize': '36px',
                    'fontWeight': 'bold',
                    'color': 'white'
                })
            ]),
            
            # Title
            html.H1("VARIANT GROUP", style={
                'fontSize': '28px',
                'fontWeight': '700',
                'color': colors['text_primary'],
                'margin': '16px 0 0 0',
                'letterSpacing': '3px'
            }),
            
            # Subtitle
            html.P("Sign in to access your dashboards", style={
                'color': colors['text_secondary'],
                'fontSize': '14px',
                'margin': '8px 0 40px 0'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),
        
        # Login form
        html.Div([
            # Username input
            html.Div([
                html.Label("Username", style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'color': colors['text_primary'],
                    'fontWeight': '500'
                }),
                dcc.Input(
                    id='username-input',
                    type='text',
                    placeholder='Enter your username',
                    style={
                        'width': '100%',
                        'padding': '12px',
                        'borderRadius': '8px',
                        'border': f'1px solid {colors["border"]}',
                        'background': colors['input_bg'],
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'boxSizing': 'border-box'
                    }
                )
            ], style={'marginBottom': '16px'}),
            
            # Password input
            html.Div([
                html.Label("Password", style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'color': colors['text_primary'],
                    'fontWeight': '500'
                }),
                dcc.Input(
                    id='password-input',
                    type='password',
                    placeholder='Enter your password',
                    style={
                        'width': '100%',
                        'padding': '12px',
                        'borderRadius': '8px',
                        'border': f'1px solid {colors["border"]}',
                        'background': colors['input_bg'],
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'boxSizing': 'border-box'
                    }
                )
            ], style={'marginBottom': '16px'}),
            
            # Remember me checkbox
            html.Div([
                dcc.Checklist(
                    id='remember-me',
                    options=[{'label': ' Remember me', 'value': 'remember'}],
                    value=[],
                    style={'color': colors['text_primary']}
                )
            ], style={'marginBottom': '24px'}),
            
            # Error message
            html.Div(id='login-error', style={
                'display': 'none',
                'marginBottom': '16px',
                'padding': '10px',
                'borderRadius': '8px',
                'background': 'rgba(248, 113, 113, 0.1)',
                'textAlign': 'center'
            }),
            
            # Sign In button
            html.Button("Sign In", id='login-btn', style={
                'width': '100%',
                'padding': '12px',
                'borderRadius': '8px',
                'border': 'none',
                'background': colors['accent'],
                'color': 'white',
                'fontSize': '16px',
                'fontWeight': '600',
                'cursor': 'pointer',
                'transition': 'all 0.2s ease'
            }),
            
            # Demo credentials box
            html.Div([
                html.Div("Demo Credentials:", style={
                    'fontWeight': '600',
                    'marginBottom': '8px',
                    'color': colors['text_primary']
                }),
                html.Div([
                    html.Span("Admin: ", style={'fontWeight': '500'}),
                    html.Code("admin", style={
                        'background': colors['surface'],
                        'padding': '2px 6px',
                        'borderRadius': '4px'
                    }),
                    " / ",
                    html.Code("admin123", style={
                        'background': colors['surface'],
                        'padding': '2px 6px',
                        'borderRadius': '4px'
                    })
                ], style={'marginBottom': '4px', 'color': colors['text_secondary']}),
                html.Div([
                    html.Span("Viewer: ", style={'fontWeight': '500'}),
                    html.Code("viewer", style={
                        'background': colors['surface'],
                        'padding': '2px 6px',
                        'borderRadius': '4px'
                    }),
                    " / ",
                    html.Code("viewer123", style={
                        'background': colors['surface'],
                        'padding': '2px 6px',
                        'borderRadius': '4px'
                    })
                ], style={'color': colors['text_secondary']})
            ], style={
                'marginTop': '24px',
                'padding': '16px',
                'background': f'rgba(20, 184, 166, 0.1)',
                'border': f'1px solid {colors["accent"]}',
                'borderRadius': '8px'
            })
        ], style={
            'width': '100%',
            'maxWidth': '400px',
            'padding': '32px',
            'background': colors['card_bg'],
            'borderRadius': '12px',
            'border': f'1px solid {colors["border"]}'
        })
    ], id='app-container', style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'minHeight': '100vh',
        'background': colors['background'],
        'padding': '20px'
    })
