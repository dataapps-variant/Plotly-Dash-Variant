"""
Login Page for Variant Analytics Dashboard (Dash Version)
"""

from dash import html, dcc
from theme import get_theme_colors


def create_login_layout(theme='dark'):
    """Create the login page layout"""
    colors = get_theme_colors(theme)
    theme_icon = "☀️" if theme == "dark" else "🌙"
    theme_text = "Light Mode" if theme == "dark" else "Dark Mode"
    
    return html.Div([
        # Top right menu
        html.Div([
            html.Button(
                f"{theme_icon} {theme_text}",
                id='theme-toggle',
                className='btn-secondary',
                style={'fontSize': '14px'}
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'flex-end',
            'padding': '16px',
        }),
        
        # Logo and header
        html.Div([
            html.Div([
                html.Div('V', style={
                    'width': '80px',
                    'height': '80px',
                    'background': colors['accent'],
                    'borderRadius': '12px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'fontSize': '36px',
                    'fontWeight': 'bold',
                    'color': 'white',
                }),
                html.H1('VARIANT GROUP', style={
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'color': colors['text_primary'],
                    'margin': '16px 0 0 0',
                    'letterSpacing': '3px',
                }),
                html.P('Sign in to access your dashboards', style={
                    'fontSize': '14px',
                    'color': colors['text_secondary'],
                    'margin': '8px 0 40px 0',
                }),
            ], className='logo-header'),
        ]),
        
        # Login form
        html.Div([
            html.Div([
                html.Label('Username', style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'color': colors['text_secondary'],
                    'fontSize': '14px',
                }),
                dcc.Input(
                    id='username-input',
                    type='text',
                    placeholder='Enter your username',
                    style={
                        'width': '100%',
                        'padding': '12px',
                        'marginBottom': '16px',
                        'background': colors['input_bg'],
                        'border': f'1px solid {colors["border"]}',
                        'borderRadius': '8px',
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'boxSizing': 'border-box',
                    }
                ),
                
                html.Label('Password', style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'color': colors['text_secondary'],
                    'fontSize': '14px',
                }),
                dcc.Input(
                    id='password-input',
                    type='password',
                    placeholder='Enter your password',
                    style={
                        'width': '100%',
                        'padding': '12px',
                        'marginBottom': '16px',
                        'background': colors['input_bg'],
                        'border': f'1px solid {colors["border"]}',
                        'borderRadius': '8px',
                        'color': colors['text_primary'],
                        'fontSize': '14px',
                        'boxSizing': 'border-box',
                    }
                ),
                
                dcc.Checklist(
                    id='remember-me',
                    options=[{'label': ' Remember me', 'value': 'remember'}],
                    value=[],
                    style={
                        'marginBottom': '24px',
                        'color': colors['text_primary'],
                    }
                ),
                
                html.Button(
                    'Sign In',
                    id='login-button',
                    className='btn-primary',
                    style={
                        'width': '100%',
                        'padding': '12px',
                        'fontSize': '16px',
                        'fontWeight': '500',
                    }
                ),
                
                html.Div(id='login-error', style={'marginTop': '16px'}),
                
            ], style={
                'background': colors['card_bg'],
                'padding': '32px',
                'borderRadius': '12px',
                'border': f'1px solid {colors["border"]}',
                'maxWidth': '400px',
                'margin': '0 auto',
            }),
            
            # Demo credentials box
            html.Div([
                html.Strong('Demo Credentials:', style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'color': colors['text_primary'],
                }),
                html.Ul([
                    html.Li('Admin: admin / admin123'),
                    html.Li('Viewer: viewer / viewer123'),
                ], style={
                    'margin': '0',
                    'paddingLeft': '20px',
                    'color': colors['text_secondary'],
                })
            ], className='alert alert-info', style={
                'maxWidth': '400px',
                'margin': '24px auto 0',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderLeft': f'4px solid {colors["accent"]}',
                'borderRadius': '8px',
                'padding': '16px',
            }),
            
        ], style={
            'maxWidth': '500px',
            'margin': '0 auto',
            'padding': '0 20px',
        }),
        
    ], style={
        'minHeight': '100vh',
        'background': colors['background'],
    })
