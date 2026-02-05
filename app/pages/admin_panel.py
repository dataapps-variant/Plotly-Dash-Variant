"""
Admin Panel for Variant Analytics Dashboard - Plotly Dash Version
"""

from dash import html, dcc, Input, Output, State, callback, no_update, dash_table
import pandas as pd
from theme import get_theme_colors
from auth import (
    get_all_users, add_user, delete_user, update_user,
    get_role_display, get_readonly_users_for_dashboard
)
from config import DASHBOARDS, ROLE_OPTIONS, ROLE_DISPLAY


def create_admin_layout(theme="dark"):
    """Create the admin panel layout"""
    
    colors = get_theme_colors(theme)
    users = get_all_users()
    
    # Build users table data
    user_data = []
    for user_id, user_info in users.items():
        user_data.append({
            "User ID": user_id,
            "Name": user_info["name"],
            "Role": get_role_display(user_info["role"]),
            "Password": "••••••••"
        })
    
    users_df = pd.DataFrame(user_data)
    
    # Build dashboard access data
    access_data = []
    for dashboard in DASHBOARDS:
        readonly_users = get_readonly_users_for_dashboard(dashboard["id"])
        users_display = ", ".join(readonly_users) if readonly_users else "—"
        access_data.append({
            "Dashboard": dashboard["name"],
            "Read Only Users": users_display
        })
    
    access_df = pd.DataFrame(access_data)
    
    return html.Div([
        # Close button
        html.Div([
            html.A(
                html.Button("✕ Close", className='btn btn-secondary'),
                href='/landing'
            )
        ], style={
            'position': 'absolute',
            'top': '20px',
            'right': '40px'
        }),
        
        # Logo and header
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
            }),
            html.H1("VARIANT GROUP", style={
                'fontSize': '28px',
                'fontWeight': '700',
                'color': colors['text_primary'],
                'margin': '16px 0 0 0',
                'letterSpacing': '3px'
            }),
            html.H2("Admin Panel", style={
                'fontSize': '20px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'margin': '8px 0 40px 0'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),
        
        # Admin status message
        html.Div(id='admin-status', style={'marginBottom': '20px'}),
        
        # Users Section
        html.Div([
            html.H3("👥 Users", style={
                'color': colors['text_primary'],
                'marginBottom': '16px'
            }),
            
            dash_table.DataTable(
                id='users-table',
                columns=[{"name": col, "id": col} for col in users_df.columns],
                data=users_df.to_dict('records'),
                style_table={
                    'overflowX': 'auto',
                    'borderRadius': '8px',
                    'border': f'1px solid {colors["border"]}'
                },
                style_header={
                    'backgroundColor': colors['table_header_bg'],
                    'color': colors['text_primary'],
                    'fontWeight': '600',
                    'borderBottom': f'2px solid {colors["border"]}'
                },
                style_cell={
                    'backgroundColor': colors['card_bg'],
                    'color': colors['text_primary'],
                    'padding': '12px',
                    'border': f'1px solid {colors["border"]}'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': colors['table_row_odd']
                    }
                ],
                row_selectable='single',
                selected_rows=[]
            ),
            
            # Action buttons
            html.Div([
                html.Button("✏️ Edit Selected", id='edit-user-btn', className='btn btn-secondary',
                           style={'marginRight': '10px'}),
                html.Button("🗑️ Delete Selected", id='delete-user-btn', className='btn btn-secondary',
                           style={'background': colors['danger']})
            ], style={'marginTop': '16px'})
        ], style={
            'background': colors['card_bg'],
            'border': f'1px solid {colors["border"]}',
            'borderRadius': '12px',
            'padding': '20px',
            'marginBottom': '24px'
        }),
        
        # Dashboard Access Section
        html.Div([
            html.H3("📊 Dashboard Access", style={
                'color': colors['text_primary'],
                'marginBottom': '8px'
            }),
            html.P("Note: Admin users have access to all dashboards.", style={
                'color': colors['text_secondary'],
                'fontSize': '14px',
                'marginBottom': '16px'
            }),
            
            dash_table.DataTable(
                id='access-table',
                columns=[{"name": col, "id": col} for col in access_df.columns],
                data=access_df.to_dict('records'),
                style_table={
                    'overflowX': 'auto',
                    'borderRadius': '8px',
                    'border': f'1px solid {colors["border"]}'
                },
                style_header={
                    'backgroundColor': colors['table_header_bg'],
                    'color': colors['text_primary'],
                    'fontWeight': '600',
                    'borderBottom': f'2px solid {colors["border"]}'
                },
                style_cell={
                    'backgroundColor': colors['card_bg'],
                    'color': colors['text_primary'],
                    'padding': '12px',
                    'border': f'1px solid {colors["border"]}'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': colors['table_row_odd']
                    }
                ]
            )
        ], style={
            'background': colors['card_bg'],
            'border': f'1px solid {colors["border"]}',
            'borderRadius': '12px',
            'padding': '20px',
            'marginBottom': '24px'
        }),
        
        # Add New User Section
        html.Details([
            html.Summary("➕ Add New User", style={
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '600',
                'padding': '12px',
                'color': colors['text_primary']
            }),
            
            html.Div([
                html.Div([
                    # Left column
                    html.Div([
                        html.Div([
                            html.Label("User Name", style={
                                'display': 'block',
                                'marginBottom': '8px',
                                'color': colors['text_primary'],
                                'fontWeight': '500'
                            }),
                            dcc.Input(
                                id='new-user-name',
                                type='text',
                                placeholder='Display Name',
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'borderRadius': '8px',
                                    'border': f'1px solid {colors["border"]}',
                                    'background': colors['input_bg'],
                                    'color': colors['text_primary']
                                }
                            )
                        ], style={'marginBottom': '16px'}),
                        
                        html.Div([
                            html.Label("User ID (Login)", style={
                                'display': 'block',
                                'marginBottom': '8px',
                                'color': colors['text_primary'],
                                'fontWeight': '500'
                            }),
                            dcc.Input(
                                id='new-user-id',
                                type='text',
                                placeholder='Login ID',
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'borderRadius': '8px',
                                    'border': f'1px solid {colors["border"]}',
                                    'background': colors['input_bg'],
                                    'color': colors['text_primary']
                                }
                            )
                        ])
                    ], style={'flex': '1', 'paddingRight': '20px'}),
                    
                    # Right column
                    html.Div([
                        html.Div([
                            html.Label("Password", style={
                                'display': 'block',
                                'marginBottom': '8px',
                                'color': colors['text_primary'],
                                'fontWeight': '500'
                            }),
                            dcc.Input(
                                id='new-user-password',
                                type='password',
                                placeholder='Password',
                                style={
                                    'width': '100%',
                                    'padding': '10px',
                                    'borderRadius': '8px',
                                    'border': f'1px solid {colors["border"]}',
                                    'background': colors['input_bg'],
                                    'color': colors['text_primary']
                                }
                            )
                        ], style={'marginBottom': '16px'}),
                        
                        html.Div([
                            html.Label("Role", style={
                                'display': 'block',
                                'marginBottom': '8px',
                                'color': colors['text_primary'],
                                'fontWeight': '500'
                            }),
                            dcc.Dropdown(
                                id='new-user-role',
                                options=[
                                    {'label': ROLE_DISPLAY[r], 'value': r}
                                    for r in ROLE_OPTIONS
                                ],
                                value='readonly',
                                clearable=False
                            )
                        ])
                    ], style={'flex': '1'})
                ], style={
                    'display': 'flex',
                    'marginBottom': '16px'
                }),
                
                # Dashboard access (for readonly)
                html.Div([
                    html.Label("Dashboard Access (for Read Only users)", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'color': colors['text_primary'],
                        'fontWeight': '500'
                    }),
                    dcc.Checklist(
                        id='new-user-dashboards',
                        options=[
                            {'label': d['name'], 'value': d['id']}
                            for d in DASHBOARDS
                        ],
                        value=[],
                        labelStyle={'display': 'block', 'padding': '4px 0'},
                        inputStyle={'marginRight': '8px'}
                    )
                ], id='new-user-dashboards-container', style={'marginBottom': '20px'}),
                
                html.Button("Create User", id='create-user-btn', className='btn',
                           style={'width': '100%'})
            ], style={'padding': '16px'})
        ], style={
            'background': colors['card_bg'],
            'border': f'1px solid {colors["border"]}',
            'borderRadius': '8px',
            'marginBottom': '24px'
        })
        
    ], id='app-container', style={
        'minHeight': '100vh',
        'background': colors['background'],
        'padding': '20px 40px',
        'position': 'relative',
        'maxWidth': '1000px',
        'margin': '0 auto'
    })


# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output('admin-status', 'children'),
    Input('create-user-btn', 'n_clicks'),
    [State('new-user-name', 'value'),
     State('new-user-id', 'value'),
     State('new-user-password', 'value'),
     State('new-user-role', 'value'),
     State('new-user-dashboards', 'value'),
     State('theme-store', 'data')],
    prevent_initial_call=True
)
def handle_create_user(n_clicks, name, user_id, password, role, dashboards, theme):
    """Handle create user button"""
    if not n_clicks:
        return no_update
    
    colors = get_theme_colors(theme)
    
    if not all([name, user_id, password]):
        return html.Div("Please fill all required fields", className='alert alert-warning')
    
    dashboard_access = dashboards if role == 'readonly' else 'all'
    success, msg = add_user(user_id, password, role, name, dashboard_access)
    
    if success:
        return html.Div(msg, className='alert alert-success')
    else:
        return html.Div(msg, className='alert alert-error')


@callback(
    Output('admin-status', 'children', allow_duplicate=True),
    Input('delete-user-btn', 'n_clicks'),
    State('users-table', 'selected_rows'),
    State('users-table', 'data'),
    prevent_initial_call=True
)
def handle_delete_user(n_clicks, selected_rows, data):
    """Handle delete user button"""
    if not n_clicks or not selected_rows:
        return no_update
    
    user_id = data[selected_rows[0]]["User ID"]
    success, msg = delete_user(user_id)
    
    if success:
        return html.Div(msg, className='alert alert-success')
    else:
        return html.Div(msg, className='alert alert-error')


@callback(
    Output('new-user-dashboards-container', 'style'),
    Input('new-user-role', 'value')
)
def toggle_dashboard_selection(role):
    """Show/hide dashboard selection based on role"""
    if role == 'readonly':
        return {'marginBottom': '20px', 'display': 'block'}
    else:
        return {'marginBottom': '20px', 'display': 'none'}
