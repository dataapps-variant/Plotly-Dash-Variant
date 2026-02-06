"""
Admin Panel for Variant Analytics Dashboard (Dash Version)
"""

from dash import html, dcc, dash_table
from theme import get_theme_colors
from config import DASHBOARDS, ROLE_OPTIONS, ROLE_DISPLAY
from auth import get_all_users, get_role_display, get_readonly_users_for_dashboard


def create_admin_layout(user, theme='dark'):
    """Create the admin panel layout"""
    colors = get_theme_colors(theme)
    
    users = get_all_users()
    
    # Build users table data
    user_data = []
    for user_id, user_info in users.items():
        user_data.append({
            'User ID': user_id,
            'Name': user_info['name'],
            'Role': get_role_display(user_info['role']),
            'Password': '••••••••',
        })
    
    # Build dashboard access data
    access_data = []
    for dashboard in DASHBOARDS:
        readonly_users = get_readonly_users_for_dashboard(dashboard['id'])
        users_display = ', '.join(readonly_users) if readonly_users else '—'
        access_data.append({
            'Dashboard': dashboard['name'],
            'Read Only Users': users_display,
        })
    
    return html.Div([
        # Close button
        html.Div([
            dcc.Link(
                '✕ Close',
                href='/',
                className='btn-secondary',
                style={'textDecoration': 'none', 'padding': '8px 16px'}
            ),
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
            html.H2('Admin Panel', style={
                'fontSize': '20px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'margin': '16px 0 40px 0',
            }),
        ], className='logo-header'),
        
        # Content
        html.Div([
            # Users Section
            html.H3('👥 Users', style={
                'fontSize': '18px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'marginBottom': '16px',
            }),
            
            dash_table.DataTable(
                id='users-table',
                columns=[
                    {'name': 'User ID', 'id': 'User ID'},
                    {'name': 'Name', 'id': 'Name'},
                    {'name': 'Role', 'id': 'Role'},
                    {'name': 'Password', 'id': 'Password'},
                ],
                data=user_data,
                style_table={
                    'overflowX': 'auto',
                    'borderRadius': '8px',
                    'border': f'1px solid {colors["border"]}',
                },
                style_header={
                    'backgroundColor': colors['table_header_bg'],
                    'color': colors['text_primary'],
                    'fontWeight': '600',
                    'borderBottom': f'2px solid {colors["border"]}',
                },
                style_cell={
                    'backgroundColor': colors['card_bg'],
                    'color': colors['text_primary'],
                    'padding': '12px 16px',
                    'borderBottom': f'1px solid {colors["border"]}',
                    'textAlign': 'left',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': colors['table_row_odd'],
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': colors['table_row_even'],
                    },
                ],
            ),
            
            html.Hr(style={'margin': '32px 0', 'border': 'none', 'borderTop': f'1px solid {colors["border"]}'}),
            
            # Dashboard Access Section
            html.H3('📊 Dashboard Access', style={
                'fontSize': '18px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'marginBottom': '8px',
            }),
            html.P('Note: Admin users have access to all dashboards.', style={
                'fontSize': '14px',
                'color': colors['text_secondary'],
                'marginBottom': '16px',
            }),
            
            dash_table.DataTable(
                id='access-table',
                columns=[
                    {'name': 'Dashboard', 'id': 'Dashboard'},
                    {'name': 'Read Only Users', 'id': 'Read Only Users'},
                ],
                data=access_data,
                style_table={
                    'overflowX': 'auto',
                    'borderRadius': '8px',
                    'border': f'1px solid {colors["border"]}',
                },
                style_header={
                    'backgroundColor': colors['table_header_bg'],
                    'color': colors['text_primary'],
                    'fontWeight': '600',
                    'borderBottom': f'2px solid {colors["border"]}',
                },
                style_cell={
                    'backgroundColor': colors['card_bg'],
                    'color': colors['text_primary'],
                    'padding': '12px 16px',
                    'borderBottom': f'1px solid {colors["border"]}',
                    'textAlign': 'left',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': colors['table_row_odd'],
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': colors['table_row_even'],
                    },
                ],
            ),
            
            html.Hr(style={'margin': '32px 0', 'border': 'none', 'borderTop': f'1px solid {colors["border"]}'}),
            
            # Add New User Section
            html.Details([
                html.Summary('➕ Add New User', style={
                    'cursor': 'pointer',
                    'fontSize': '18px',
                    'fontWeight': '600',
                    'color': colors['text_primary'],
                    'padding': '12px 16px',
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'borderRadius': '8px',
                }),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('User Name', style={'color': colors['text_secondary'], 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Input(id='new-user-name', type='text', placeholder='Display Name', style={
                                'width': '100%', 'padding': '10px', 'borderRadius': '8px',
                                'border': f'1px solid {colors["border"]}', 'background': colors['input_bg'],
                                'color': colors['text_primary'], 'boxSizing': 'border-box',
                            }),
                        ], style={'flex': '1', 'marginRight': '16px'}),
                        html.Div([
                            html.Label('User ID', style={'color': colors['text_secondary'], 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Input(id='new-user-id', type='text', placeholder='Login ID', style={
                                'width': '100%', 'padding': '10px', 'borderRadius': '8px',
                                'border': f'1px solid {colors["border"]}', 'background': colors['input_bg'],
                                'color': colors['text_primary'], 'boxSizing': 'border-box',
                            }),
                        ], style={'flex': '1'}),
                    ], style={'display': 'flex', 'marginBottom': '16px'}),
                    
                    html.Div([
                        html.Div([
                            html.Label('Password', style={'color': colors['text_secondary'], 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Input(id='new-user-password', type='password', style={
                                'width': '100%', 'padding': '10px', 'borderRadius': '8px',
                                'border': f'1px solid {colors["border"]}', 'background': colors['input_bg'],
                                'color': colors['text_primary'], 'boxSizing': 'border-box',
                            }),
                        ], style={'flex': '1', 'marginRight': '16px'}),
                        html.Div([
                            html.Label('Role', style={'color': colors['text_secondary'], 'marginBottom': '8px', 'display': 'block'}),
                            dcc.Dropdown(
                                id='new-user-role',
                                options=[{'label': ROLE_DISPLAY[r], 'value': r} for r in ROLE_OPTIONS],
                                value='readonly',
                                style={'borderRadius': '8px'},
                            ),
                        ], style={'flex': '1'}),
                    ], style={'display': 'flex', 'marginBottom': '16px'}),
                    
                    html.Button('Create User', id='create-user-btn', className='btn-primary', style={
                        'width': '100%', 'padding': '12px',
                    }),
                    
                    html.Div(id='create-user-message', style={'marginTop': '16px'}),
                    
                ], style={
                    'padding': '20px',
                    'background': colors['card_bg'],
                    'border': f'1px solid {colors["border"]}',
                    'borderTop': 'none',
                    'borderRadius': '0 0 8px 8px',
                }),
            ], style={'marginTop': '0'}),
            
        ], style={
            'maxWidth': '1000px',
            'margin': '0 auto',
            'padding': '0 20px 40px',
        }),
        
    ], style={
        'minHeight': '100vh',
        'background': colors['background'],
    })
