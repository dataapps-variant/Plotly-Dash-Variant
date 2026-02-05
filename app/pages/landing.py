"""
Landing Page (Dashboard Hub) for Variant Analytics Dashboard - Plotly Dash Version
"""

from dash import html, dcc
from theme import get_theme_colors
from auth import get_current_user, is_admin
from config import DASHBOARDS
from bigquery_client import get_cache_info


def create_landing_layout(theme="dark"):
    """Create the landing page layout with dashboard table"""
    
    colors = get_theme_colors(theme)
    user = get_current_user()
    cache_info = get_cache_info()
    
    if not user:
        user = {'name': 'Guest', 'role': 'readonly'}
    
    # Build dashboard rows
    dashboard_rows = []
    for dashboard in DASHBOARDS:
        is_enabled = dashboard.get("enabled", False)
        status = "✅ Active" if is_enabled else "⏸️ Disabled"
        bq_display = cache_info.get("last_bq_refresh", "--") if is_enabled else "--"
        gcs_display = cache_info.get("last_gcs_refresh", "--") if is_enabled else "--"
        
        if is_enabled:
            # Clickable button for enabled dashboards
            name_cell = html.Button(
                dashboard["name"],
                id={'type': 'nav-btn', 'page': dashboard['id']},
                style={
                    'background': 'transparent',
                    'border': 'none',
                    'color': colors['accent'],
                    'cursor': 'pointer',
                    'fontWeight': '500',
                    'fontSize': '14px',
                    'padding': '0',
                    'textAlign': 'left',
                    'textDecoration': 'underline'
                }
            )
        else:
            name_cell = html.Span(dashboard["name"], style={'color': colors['text_secondary']})
        
        dashboard_rows.append(
            html.Tr([
                html.Td(name_cell, style={'padding': '12px 16px'}),
                html.Td(status, style={'padding': '12px 16px'}),
                html.Td(bq_display, style={'padding': '12px 16px'}),
                html.Td(gcs_display, style={'padding': '12px 16px'})
            ], style={
                'borderBottom': f'1px solid {colors["border"]}'
            })
        )
    
    # Build menu items
    menu_items = [
        html.Button(
            f"{'☀️' if theme == 'dark' else '🌙'} {'Light' if theme == 'dark' else 'Dark'} Mode",
            id='theme-toggle-btn',
            style={
                'display': 'block',
                'width': '100%',
                'padding': '10px 16px',
                'background': 'transparent',
                'border': 'none',
                'color': colors['text_primary'],
                'cursor': 'pointer',
                'textAlign': 'left',
                'fontSize': '14px'
            }
        )
    ]
    
    if is_admin():
        menu_items.extend([
            html.Hr(style={'margin': '8px 0', 'borderColor': colors['border']}),
            html.A(
                "🔧 Admin Panel",
                href='/admin',
                style={
                    'display': 'block',
                    'padding': '10px 16px',
                    'color': colors['text_primary'],
                    'textDecoration': 'none',
                    'fontSize': '14px'
                }
            )
        ])
    
    menu_items.extend([
        html.Hr(style={'margin': '8px 0', 'borderColor': colors['border']}),
        html.Div([
            html.Div(f"User: {user['name']}", style={
                'fontWeight': '500',
                'marginBottom': '4px'
            }),
            html.Div(f"Role: {'Admin' if user['role'] == 'admin' else 'Read Only'}", style={
                'color': colors['text_secondary'],
                'fontSize': '12px'
            })
        ], style={'padding': '10px 16px'}),
        html.Hr(style={'margin': '8px 0', 'borderColor': colors['border']}),
        html.Button(
            "🚪 Logout",
            id='logout-btn',
            style={
                'display': 'block',
                'width': '100%',
                'padding': '10px 16px',
                'background': 'transparent',
                'border': 'none',
                'color': colors['danger'],
                'cursor': 'pointer',
                'textAlign': 'left',
                'fontSize': '14px'
            }
        )
    ])
    
    return html.Div([
        # Top right menu
        html.Div([
            html.Details([
                html.Summary("⋮", style={
                    'cursor': 'pointer',
                    'fontSize': '24px',
                    'color': colors['text_primary'],
                    'listStyle': 'none',
                    'padding': '8px'
                }),
                html.Div(
                    menu_items,
                    style={
                        'position': 'absolute',
                        'right': '0',
                        'top': '100%',
                        'background': colors['card_bg'],
                        'border': f'1px solid {colors["border"]}',
                        'borderRadius': '8px',
                        'minWidth': '200px',
                        'boxShadow': '0 4px 12px rgba(0,0,0,0.2)',
                        'zIndex': '1000'
                    }
                )
            ], style={'position': 'relative'})
        ], style={
            'position': 'absolute',
            'top': '20px',
            'right': '40px'
        }),
        
        # Logo and header
        html.Div([
            # Logo
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
            }),
            
            # Title
            html.H1("VARIANT GROUP", style={
                'fontSize': '28px',
                'fontWeight': '700',
                'color': colors['text_primary'],
                'margin': '16px 0 0 0',
                'letterSpacing': '3px'
            }),
            
            # Welcome message
            html.P(f"Welcome back, {user['name']}", style={
                'color': colors['text_secondary'],
                'fontSize': '16px',
                'margin': '8px 0 0 0'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'padding': '30px 0',
            'textAlign': 'center'
        }),
        
        # Dashboard table
        html.Div([
            html.H3("📊 Available Dashboards", style={
                'color': colors['text_primary'],
                'marginBottom': '16px'
            }),
            
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Dashboard", style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}'
                        }),
                        html.Th("Status", style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}'
                        }),
                        html.Th("Last BQ Refresh", style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}'
                        }),
                        html.Th("Last GCS Refresh", style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}'
                        })
                    ])
                ]),
                html.Tbody(dashboard_rows)
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'background': colors['card_bg'],
                'borderRadius': '8px',
                'overflow': 'hidden',
                'color': colors['text_primary']
            })
        ], style={
            'maxWidth': '900px',
            'margin': '0 auto',
            'padding': '0 20px'
        })
    ], id='app-container', style={
        'minHeight': '100vh',
        'background': colors['background'],
        'padding': '20px 40px',
        'position': 'relative'
    })
