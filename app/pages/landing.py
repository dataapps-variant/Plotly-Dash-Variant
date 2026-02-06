"""
Landing Page (Dashboard Hub) for Variant Analytics Dashboard (Dash Version)
"""

from dash import html, dcc
from theme import get_theme_colors
from config import DASHBOARDS
from bigquery_client import get_cache_info
from auth import is_admin


def create_landing_layout(user, theme='dark'):
    """Create the landing page layout"""
    colors = get_theme_colors(theme)
    cache_info = get_cache_info()
    
    theme_icon = "☀️" if theme == "dark" else "🌙"
    theme_text = "Light Mode" if theme == "dark" else "Dark Mode"
    
    # Build dashboard rows
    dashboard_rows = []
    bq_refresh = cache_info.get("last_bq_refresh", "--")
    gcs_refresh = cache_info.get("last_gcs_refresh", "--")
    
    for dashboard in DASHBOARDS:
        is_enabled = dashboard.get("enabled", False)
        status = "✅ Active" if is_enabled else "⏸️ Disabled"
        bq_display = bq_refresh if is_enabled else "--"
        gcs_display = gcs_refresh if is_enabled else "--"
        
        if is_enabled:
            name_element = dcc.Link(
                dashboard["name"],
                href=f'/{dashboard["id"]}',
                style={
                    'color': colors['accent'],
                    'textDecoration': 'none',
                    'fontWeight': '500',
                }
            )
        else:
            name_element = html.Span(
                dashboard["name"],
                style={'color': colors['text_secondary']}
            )
        
        dashboard_rows.append(
            html.Tr([
                html.Td(name_element, style={
                    'padding': '12px 16px',
                    'borderBottom': f'1px solid {colors["border"]}',
                }),
                html.Td(status, style={
                    'padding': '12px 16px',
                    'borderBottom': f'1px solid {colors["border"]}',
                }),
                html.Td(bq_display, style={
                    'padding': '12px 16px',
                    'borderBottom': f'1px solid {colors["border"]}',
                }),
                html.Td(gcs_display, style={
                    'padding': '12px 16px',
                    'borderBottom': f'1px solid {colors["border"]}',
                }),
            ])
        )
    
    # Build menu items
    menu_items = [
        html.Button(
            f"{theme_icon} {theme_text}",
            id='theme-toggle',
            className='menu-item',
            style={'width': '100%', 'textAlign': 'left', 'border': 'none', 'background': 'none'}
        ),
    ]
    
    if is_admin(user):
        menu_items.append(html.Hr(style={'margin': '8px 0', 'border': 'none', 'borderTop': f'1px solid {colors["border"]}'}))
        menu_items.append(
            dcc.Link(
                '🔧 Admin Panel',
                href='/admin',
                className='menu-item',
                style={'display': 'block', 'textDecoration': 'none', 'color': colors['text_primary']}
            )
        )
    
    menu_items.extend([
        html.Hr(style={'margin': '8px 0', 'border': 'none', 'borderTop': f'1px solid {colors["border"]}'}),
        html.Div([
            html.Strong('User: ', style={'color': colors['text_secondary']}),
            html.Span(user['name'], style={'color': colors['text_primary']}),
        ], style={'padding': '8px 16px'}),
        html.Div([
            html.Strong('Role: ', style={'color': colors['text_secondary']}),
            html.Span('Admin' if user['role'] == 'admin' else 'Read Only', style={'color': colors['text_primary']}),
        ], style={'padding': '8px 16px'}),
        html.Hr(style={'margin': '8px 0', 'border': 'none', 'borderTop': f'1px solid {colors["border"]}'}),
        html.Button(
            '🚪 Logout',
            id='logout-button',
            className='menu-item',
            style={'width': '100%', 'textAlign': 'left', 'border': 'none', 'background': 'none', 'cursor': 'pointer'}
        ),
    ])
    
    return html.Div([
        # Top right menu
        html.Div([
            html.Div([
                html.Button('⋮', style={
                    'fontSize': '20px',
                    'background': 'none',
                    'border': 'none',
                    'color': colors['text_primary'],
                    'cursor': 'pointer',
                    'padding': '8px 12px',
                }),
                html.Div(menu_items, className='dropdown-content', style={
                    'display': 'none',
                    'position': 'absolute',
                    'right': '0',
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'borderRadius': '8px',
                    'minWidth': '180px',
                    'boxShadow': '0 4px 12px rgba(0,0,0,0.15)',
                    'zIndex': '1000',
                    'padding': '8px 0',
                }),
            ], className='dropdown', style={'position': 'relative'})
        ], style={
            'display': 'flex',
            'justifyContent': 'flex-end',
            'padding': '16px',
        }),
        
        # Logo and header
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
            html.P(f'Welcome back, {user["name"]}', style={
                'fontSize': '16px',
                'color': colors['text_secondary'],
                'margin': '8px 0 0 0',
            }),
        ], className='logo-header'),
        
        html.Br(),
        
        # Dashboard table
        html.Div([
            html.H2('📊 Available Dashboards', style={
                'fontSize': '20px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'marginBottom': '16px',
            }),
            
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th('Dashboard', style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}',
                            'background': colors['table_header_bg'],
                        }),
                        html.Th('Status', style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}',
                            'background': colors['table_header_bg'],
                        }),
                        html.Th('Last BQ Refresh', style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}',
                            'background': colors['table_header_bg'],
                        }),
                        html.Th('Last GCS Refresh', style={
                            'padding': '12px 16px',
                            'textAlign': 'left',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'borderBottom': f'2px solid {colors["border"]}',
                            'background': colors['table_header_bg'],
                        }),
                    ])
                ]),
                html.Tbody(dashboard_rows),
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'background': colors['card_bg'],
                'borderRadius': '8px',
                'overflow': 'hidden',
                'border': f'1px solid {colors["border"]}',
            }),
            
        ], style={
            'maxWidth': '1000px',
            'margin': '0 auto',
            'padding': '0 20px',
        }),
        
    ], style={
        'minHeight': '100vh',
        'background': colors['background'],
    })
