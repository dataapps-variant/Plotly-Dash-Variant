"""
Filter Components for Variant Analytics Dashboard - Plotly Dash Version
"""

from dash import html, dcc
from config import BC_OPTIONS, COHORT_OPTIONS, METRICS_CONFIG, DEFAULT_BC, DEFAULT_COHORT, DEFAULT_PLAN
from theme import get_theme_colors


def get_plans_by_app(plan_groups):
    """
    Group plans by App_Name
    
    Input: {"App_Name": [...], "Plan_Name": [...]}
    Output: {"AT": ["AT001", "AT002"], "CL": ["CL001"], ...}
    """
    result = {}
    for app, plan in zip(plan_groups["App_Name"], plan_groups["Plan_Name"]):
        if app not in result:
            result[app] = []
        if plan not in result[app]:
            result[app].append(plan)
    return result


def create_plan_checklist(app_name, plans, key_prefix="", default_plan=DEFAULT_PLAN, theme="dark"):
    """Create a checklist for a single app's plans"""
    colors = get_theme_colors(theme)
    
    # Determine default selected plans
    default_values = [plan for plan in plans if plan == default_plan]
    
    return html.Div([
        html.Div(app_name, className='filter-title'),
        html.Div([
            dcc.Checklist(
                id={'type': f'{key_prefix}plan_checklist', 'app': app_name},
                options=[{'label': plan, 'value': plan} for plan in sorted(plans)],
                value=default_values,
                labelStyle={'display': 'block', 'padding': '4px 0', 'cursor': 'pointer'},
                inputStyle={'marginRight': '8px'}
            )
        ], className='checklist-container')
    ], style={'flex': '1', 'minWidth': '150px', 'maxWidth': '200px'})


def create_metrics_checklist(key_prefix="", theme="dark"):
    """Create a checklist for metrics selection"""
    colors = get_theme_colors(theme)
    
    metrics_options = [
        {'label': METRICS_CONFIG[metric]["display"], 'value': metric}
        for metric in METRICS_CONFIG.keys()
    ]
    
    return html.Div([
        html.Div("Metrics", className='filter-title'),
        html.Div([
            dcc.Checklist(
                id=f'{key_prefix}metrics_checklist',
                options=metrics_options,
                value=list(METRICS_CONFIG.keys()),  # All selected by default
                labelStyle={'display': 'block', 'padding': '4px 0', 'cursor': 'pointer'},
                inputStyle={'marginRight': '8px'}
            )
        ], className='checklist-container', style={'maxHeight': '420px'})
    ])


def create_filter_layout(plan_groups, min_date, max_date, key_prefix="", theme="dark"):
    """
    Create the complete filter layout
    
    Returns a Dash html.Div component with all filters
    """
    colors = get_theme_colors(theme)
    
    # Group plans by App
    plans_by_app = get_plans_by_app(plan_groups)
    app_names = sorted(plans_by_app.keys())
    
    # Create plan checklists for each app
    plan_checklists = []
    for app_name in app_names:
        plans = sorted(plans_by_app.get(app_name, []))
        plan_checklists.append(
            create_plan_checklist(app_name, plans, key_prefix, DEFAULT_PLAN, theme)
        )
    
    return html.Div([
        html.Details([
            html.Summary("📊 Filters", style={
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '600',
                'padding': '12px',
                'color': colors['text_primary']
            }),
            
            html.Div([
                # Row 1: Date Range, BC, Cohort, Reset
                html.Div([
                    # Date Range
                    html.Div([
                        html.Div("Date Range", className='filter-title'),
                        html.Div([
                            dcc.DatePickerSingle(
                                id=f'{key_prefix}from_date',
                                date=min_date,
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                display_format='YYYY-MM-DD',
                                placeholder='From Date'
                            ),
                            html.Span(" to ", style={'margin': '0 8px', 'color': colors['text_secondary']}),
                            dcc.DatePickerSingle(
                                id=f'{key_prefix}to_date',
                                date=max_date,
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                display_format='YYYY-MM-DD',
                                placeholder='To Date'
                            )
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ], style={'flex': '2', 'minWidth': '300px'}),
                    
                    # Billing Cycle
                    html.Div([
                        html.Div("Billing Cycle", className='filter-title'),
                        dcc.Dropdown(
                            id=f'{key_prefix}bc_dropdown',
                            options=[{'label': str(bc), 'value': bc} for bc in BC_OPTIONS],
                            value=DEFAULT_BC,
                            clearable=False,
                            style={'width': '100%'}
                        )
                    ], style={'flex': '1', 'minWidth': '120px'}),
                    
                    # Cohort
                    html.Div([
                        html.Div("Cohort", className='filter-title'),
                        dcc.Dropdown(
                            id=f'{key_prefix}cohort_dropdown',
                            options=[{'label': c, 'value': c} for c in COHORT_OPTIONS],
                            value=DEFAULT_COHORT,
                            clearable=False,
                            style={'width': '100%'}
                        )
                    ], style={'flex': '1', 'minWidth': '120px'}),
                    
                    # Reset Button
                    html.Div([
                        html.Div("\u00A0", className='filter-title'),  # Empty title for alignment
                        html.Button("🔄 Reset", id=f'{key_prefix}reset_btn', className='btn btn-secondary',
                                   style={'width': '100%'})
                    ], style={'flex': '1', 'minWidth': '100px'})
                ], style={
                    'display': 'flex',
                    'gap': '20px',
                    'marginBottom': '20px',
                    'flexWrap': 'wrap'
                }),
                
                # Row 2: Plan Groups + Metrics
                html.Div([
                    # Plan Groups
                    html.Div([
                        html.Div("Plan Groups", className='filter-title'),
                        html.Div(
                            plan_checklists,
                            style={
                                'display': 'flex',
                                'flexWrap': 'wrap',
                                'gap': '16px'
                            }
                        )
                    ], style={'flex': '4'}),
                    
                    # Metrics
                    html.Div([
                        create_metrics_checklist(key_prefix, theme)
                    ], style={'flex': '1', 'minWidth': '200px'})
                ], style={
                    'display': 'flex',
                    'gap': '20px'
                }),
                
                # Apply Filter Button
                html.Div([
                    html.Button("✅ Apply Filter", id=f'{key_prefix}apply_btn', className='btn',
                               style={'padding': '12px 24px', 'fontSize': '14px'})
                ], style={
                    'display': 'flex',
                    'justifyContent': 'flex-end',
                    'marginTop': '20px'
                })
            ], style={'padding': '16px'})
        ], open=True, style={
            'background': colors['card_bg'],
            'border': f'1px solid {colors["border"]}',
            'borderRadius': '8px',
            'marginBottom': '20px'
        })
    ])
