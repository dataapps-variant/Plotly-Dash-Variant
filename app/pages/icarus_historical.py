"""
ICARUS - Plan (Historical) Dashboard Page - Plotly Dash Version
"""

from dash import html, dcc, Input, Output, State, callback, no_update, ALL, MATCH
from theme import get_theme_colors
from auth import get_current_user
from config import CHART_METRICS, METRICS_CONFIG, BC_OPTIONS, COHORT_OPTIONS, DEFAULT_BC, DEFAULT_COHORT, DEFAULT_PLAN
from bigquery_client import (
    load_date_bounds,
    load_plan_groups,
    load_pivot_data,
    load_all_chart_data,
    refresh_bq_to_staging,
    refresh_gcs_from_staging,
    get_cache_info
)
from filters import get_plans_by_app
from pivots import create_pivot_table
from charts import create_chart_pair_layout, build_plan_color_map


def create_icarus_layout(theme="dark"):
    """Create the ICARUS Historical dashboard layout"""
    
    colors = get_theme_colors(theme)
    user = get_current_user()
    cache_info = get_cache_info()
    
    # Load initial data
    try:
        date_bounds = load_date_bounds()
        min_date = date_bounds["min_date"]
        max_date = date_bounds["max_date"]
    except Exception as e:
        return html.Div([
            html.Div(f"Error loading date bounds: {str(e)}", className='alert alert-error')
        ], style={'padding': '40px', 'background': colors['background']})
    
    return html.Div([
        # Header
        html.Div([
            # Back button
            html.Div([
                html.Button("← Back", id='back-btn', className='btn btn-secondary')
            ], style={'flex': '1'}),
            
            # Title
            html.Div([
                html.H1("ICARUS - Plan (Historical)", style={
                    'textAlign': 'center',
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'color': colors['text_primary'],
                    'margin': '0',
                    'padding': '10px 0'
                })
            ], style={'flex': '4', 'textAlign': 'center'}),
            
            # Theme toggle and Logout
            html.Div([
                html.Button(
                    "☀️" if theme == "dark" else "🌙",
                    id='theme-toggle-btn',
                    className='btn btn-secondary',
                    style={'marginRight': '8px'}
                ),
                html.Button("Logout", id='logout-btn', className='btn btn-secondary')
            ], style={'flex': '1', 'textAlign': 'right'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),
        
        # Refresh section
        html.Div([
            # BQ Refresh
            html.Div([
                html.Button("🔄", id='refresh-bq-btn', className='btn btn-secondary', 
                           style={'marginRight': '10px', 'padding': '8px 12px'}),
                html.Span(f"BQ: {cache_info.get('last_bq_refresh', '--')}", style={
                    'fontSize': '18px',
                    'fontWeight': '700',
                    'color': colors['text_primary']
                })
            ], style={'display': 'flex', 'alignItems': 'center'}),
            
            # GCS Refresh
            html.Div([
                html.Span(f"GCS: {cache_info.get('last_gcs_refresh', '--')}", style={
                    'fontSize': '18px',
                    'fontWeight': '700',
                    'color': colors['text_primary'],
                    'marginRight': '10px'
                }),
                html.Button("🔄", id='refresh-gcs-btn', className='btn btn-secondary',
                           style={'padding': '8px 12px'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'marginBottom': '20px'
        }),
        
        # Refresh status message
        html.Div(id='refresh-status', style={'marginBottom': '16px'}),
        
        # Tabs for Active/Inactive
        html.Div([
            dcc.Tabs(id='active-inactive-tabs', value='active', children=[
                dcc.Tab(label='📈 Active', value='active', style={
                    'padding': '10px 24px',
                    'fontWeight': '500'
                }, selected_style={
                    'padding': '10px 24px',
                    'fontWeight': '500',
                    'backgroundColor': colors['accent'],
                    'color': 'white',
                    'borderRadius': '8px'
                }),
                dcc.Tab(label='📉 Inactive', value='inactive', style={
                    'padding': '10px 24px',
                    'fontWeight': '500'
                }, selected_style={
                    'padding': '10px 24px',
                    'fontWeight': '500',
                    'backgroundColor': colors['accent'],
                    'color': 'white',
                    'borderRadius': '8px'
                })
            ], style={
                'marginBottom': '20px'
            })
        ]),
        
        # Tab content container
        html.Div(id='tab-content')
        
    ], id='app-container', style={
        'minHeight': '100vh',
        'background': colors['background'],
        'padding': '20px 40px'
    })


def create_dashboard_content(active_inactive, theme="dark"):
    """Create dashboard content for Active or Inactive tab"""
    
    colors = get_theme_colors(theme)
    
    # Load plan groups
    try:
        plan_groups = load_plan_groups(active_inactive.capitalize())
        if not plan_groups["Plan_Name"]:
            return html.Div([
                html.Div(f"No {active_inactive.lower()} plans found.", className='alert alert-warning')
            ])
    except Exception as e:
        return html.Div([
            html.Div(f"Error loading plan groups: {str(e)}", className='alert alert-error')
        ])
    
    # Load date bounds
    try:
        date_bounds = load_date_bounds()
        min_date = date_bounds["min_date"]
        max_date = date_bounds["max_date"]
    except Exception as e:
        return html.Div([
            html.Div(f"Error loading dates: {str(e)}", className='alert alert-error')
        ])
    
    # Group plans by App
    plans_by_app = get_plans_by_app(plan_groups)
    app_names = sorted(plans_by_app.keys())
    
    # Create plan checklists
    plan_checklists = []
    for app_name in app_names:
        plans = sorted(plans_by_app.get(app_name, []))
        default_values = [plan for plan in plans if plan == DEFAULT_PLAN]
        
        plan_checklists.append(
            html.Div([
                html.Div(app_name, className='filter-title'),
                html.Div([
                    dcc.Checklist(
                        id={'type': f'{active_inactive}_plan_checklist', 'app': app_name},
                        options=[{'label': plan, 'value': plan} for plan in plans],
                        value=default_values,
                        labelStyle={'display': 'block', 'padding': '4px 0'},
                        inputStyle={'marginRight': '8px'}
                    )
                ], className='checklist-container')
            ], style={'flex': '1', 'minWidth': '150px', 'maxWidth': '200px'})
        )
    
    # Metrics options
    metrics_options = [
        {'label': METRICS_CONFIG[metric]["display"], 'value': metric}
        for metric in METRICS_CONFIG.keys()
    ]
    
    key_prefix = f"{active_inactive}_"
    
    return html.Div([
        # Filters
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
                                display_format='YYYY-MM-DD'
                            ),
                            html.Span(" to ", style={
                                'margin': '0 8px',
                                'color': colors['text_secondary']
                            }),
                            dcc.DatePickerSingle(
                                id=f'{key_prefix}to_date',
                                date=max_date,
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                display_format='YYYY-MM-DD'
                            )
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ], style={'flex': '2'}),
                    
                    # BC
                    html.Div([
                        html.Div("Billing Cycle", className='filter-title'),
                        dcc.Dropdown(
                            id=f'{key_prefix}bc_dropdown',
                            options=[{'label': str(bc), 'value': bc} for bc in BC_OPTIONS],
                            value=DEFAULT_BC,
                            clearable=False
                        )
                    ], style={'flex': '1', 'minWidth': '120px'}),
                    
                    # Cohort
                    html.Div([
                        html.Div("Cohort", className='filter-title'),
                        dcc.Dropdown(
                            id=f'{key_prefix}cohort_dropdown',
                            options=[{'label': c, 'value': c} for c in COHORT_OPTIONS],
                            value=DEFAULT_COHORT,
                            clearable=False
                        )
                    ], style={'flex': '1', 'minWidth': '120px'}),
                    
                    # Reset
                    html.Div([
                        html.Div("\u00A0", className='filter-title'),
                        html.Button("🔄 Reset", id=f'{key_prefix}reset_btn', 
                                   className='btn btn-secondary', style={'width': '100%'})
                    ], style={'flex': '1'})
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
                        html.Div(plan_checklists, style={
                            'display': 'flex',
                            'flexWrap': 'wrap',
                            'gap': '16px'
                        })
                    ], style={'flex': '4'}),
                    
                    # Metrics
                    html.Div([
                        html.Div("Metrics", className='filter-title'),
                        html.Div([
                            dcc.Checklist(
                                id=f'{key_prefix}metrics_checklist',
                                options=metrics_options,
                                value=list(METRICS_CONFIG.keys()),
                                labelStyle={'display': 'block', 'padding': '4px 0'},
                                inputStyle={'marginRight': '8px'}
                            )
                        ], className='checklist-container', style={'maxHeight': '420px'})
                    ], style={'flex': '1', 'minWidth': '200px'})
                ], style={
                    'display': 'flex',
                    'gap': '20px'
                }),
                
                # Apply Button
                html.Div([
                    html.Button("✅ Apply Filter", id=f'{key_prefix}apply_btn', 
                               className='btn', style={'padding': '12px 24px'})
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
        }),
        
        # Info message
        html.Div(id=f'{key_prefix}info_message', children=[
            html.Div("👆 Adjust filters above and click Apply Filter to load data.",
                    className='alert alert-info')
        ]),
        
        # Content area for pivot tables and charts
        html.Div(id=f'{key_prefix}dashboard_content')
    ])


# =============================================================================
# CALLBACKS
# =============================================================================

# Tab content callback
@callback(
    Output('tab-content', 'children'),
    Input('active-inactive-tabs', 'value'),
    State('theme-store', 'data')
)
def render_tab_content(tab_value, theme):
    """Render content based on selected tab"""
    return create_dashboard_content(tab_value, theme)


# Active tab - Apply filter callback
@callback(
    [Output('active_dashboard_content', 'children'),
     Output('active_info_message', 'style')],
    Input('active_apply_btn', 'n_clicks'),
    [State('active_from_date', 'date'),
     State('active_to_date', 'date'),
     State('active_bc_dropdown', 'value'),
     State('active_cohort_dropdown', 'value'),
     State('active_metrics_checklist', 'value'),
     State({'type': 'active_plan_checklist', 'app': ALL}, 'value'),
     State('theme-store', 'data')],
    prevent_initial_call=True
)
def apply_active_filters(n_clicks, from_date, to_date, bc, cohort, metrics, plan_values, theme):
    """Apply filters and load data for Active tab"""
    if not n_clicks:
        return no_update, no_update
    
    # Collect all selected plans
    selected_plans = []
    for pv in plan_values:
        if pv:
            selected_plans.extend(pv)
    
    # Validate
    if not metrics:
        return html.Div("⚠️ Please select at least one Metric.", className='alert alert-warning'), {'display': 'block'}
    
    if not selected_plans:
        return html.Div("⚠️ Please select at least one Plan.", className='alert alert-warning'), {'display': 'block'}
    
    colors = get_theme_colors(theme)
    
    # Load data
    try:
        # Load pivot data
        pivot_data_regular = load_pivot_data(
            from_date, to_date, bc, cohort,
            selected_plans, metrics, "Regular", "Active"
        )
        pivot_data_crystal = load_pivot_data(
            from_date, to_date, bc, cohort,
            selected_plans, metrics, "Crystal Ball", "Active"
        )
        
        # Load chart data
        chart_metric_names = [cm["metric"] for cm in CHART_METRICS]
        if "Subscriptions" not in chart_metric_names:
            chart_metric_names.append("Subscriptions")
        
        all_regular_data = load_all_chart_data(
            from_date, to_date, bc, cohort,
            selected_plans, chart_metric_names, "Regular", "Active"
        )
        all_crystal_data = load_all_chart_data(
            from_date, to_date, bc, cohort,
            selected_plans, chart_metric_names, "Crystal Ball", "Active"
        )
        
    except Exception as e:
        return html.Div(f"Error loading data: {str(e)}", className='alert alert-error'), {'display': 'block'}
    
    # Build content
    content = []
    
    # Pivot Tables
    content.append(html.Details([
        html.Summary("📊 Pivot Tables", style={
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '600',
            'padding': '12px',
            'color': colors['text_primary']
        }),
        html.Div([
            create_pivot_table(pivot_data_regular, metrics, "📊 Plan Overview (Regular)", 
                              "active_pivot_regular", theme),
            create_pivot_table(pivot_data_crystal, metrics, "🔮 Plan Overview (Crystal Ball)", 
                              "active_pivot_crystal", theme)
        ], style={'padding': '16px'})
    ], open=True, style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["border"]}',
        'borderRadius': '8px',
        'marginBottom': '20px'
    }))
    
    # Charts
    charts = []
    subs_regular = all_regular_data.get("Subscriptions", {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
    subs_crystal = all_crystal_data.get("Subscriptions", {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
    
    for idx, chart_config in enumerate(CHART_METRICS):
        display_name = chart_config["display"]
        metric = chart_config["metric"]
        format_type = chart_config["format"]
        
        if format_type == "dollar":
            display_title = f"{display_name} ($)"
        elif format_type == "percent":
            display_title = f"{display_name} (%)"
        else:
            display_title = display_name
        
        chart_data_regular = all_regular_data.get(metric, {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
        chart_data_crystal = all_crystal_data.get(metric, {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
        
        charts.append(
            create_chart_pair_layout(
                chart_data_regular,
                chart_data_crystal,
                display_title,
                format_type,
                date_range=(from_date, to_date),
                chart_key=f"active_chart_{idx}",
                subscriptions_regular=subs_regular,
                subscriptions_crystal=subs_crystal,
                theme=theme
            )
        )
    
    content.append(html.Details([
        html.Summary("📈 Charts", style={
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '600',
            'padding': '12px',
            'color': colors['text_primary']
        }),
        html.Div(charts, style={'padding': '16px'})
    ], open=True, style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["border"]}',
        'borderRadius': '8px',
        'marginBottom': '20px'
    }))
    
    return html.Div(content), {'display': 'none'}


# Inactive tab - Apply filter callback
@callback(
    [Output('inactive_dashboard_content', 'children'),
     Output('inactive_info_message', 'style')],
    Input('inactive_apply_btn', 'n_clicks'),
    [State('inactive_from_date', 'date'),
     State('inactive_to_date', 'date'),
     State('inactive_bc_dropdown', 'value'),
     State('inactive_cohort_dropdown', 'value'),
     State('inactive_metrics_checklist', 'value'),
     State({'type': 'inactive_plan_checklist', 'app': ALL}, 'value'),
     State('theme-store', 'data')],
    prevent_initial_call=True
)
def apply_inactive_filters(n_clicks, from_date, to_date, bc, cohort, metrics, plan_values, theme):
    """Apply filters and load data for Inactive tab"""
    if not n_clicks:
        return no_update, no_update
    
    # Collect all selected plans
    selected_plans = []
    for pv in plan_values:
        if pv:
            selected_plans.extend(pv)
    
    # Validate
    if not metrics:
        return html.Div("⚠️ Please select at least one Metric.", className='alert alert-warning'), {'display': 'block'}
    
    if not selected_plans:
        return html.Div("⚠️ Please select at least one Plan.", className='alert alert-warning'), {'display': 'block'}
    
    colors = get_theme_colors(theme)
    
    # Load data (same logic as active, but with "Inactive")
    try:
        pivot_data_regular = load_pivot_data(
            from_date, to_date, bc, cohort,
            selected_plans, metrics, "Regular", "Inactive"
        )
        pivot_data_crystal = load_pivot_data(
            from_date, to_date, bc, cohort,
            selected_plans, metrics, "Crystal Ball", "Inactive"
        )
        
        chart_metric_names = [cm["metric"] for cm in CHART_METRICS]
        if "Subscriptions" not in chart_metric_names:
            chart_metric_names.append("Subscriptions")
        
        all_regular_data = load_all_chart_data(
            from_date, to_date, bc, cohort,
            selected_plans, chart_metric_names, "Regular", "Inactive"
        )
        all_crystal_data = load_all_chart_data(
            from_date, to_date, bc, cohort,
            selected_plans, chart_metric_names, "Crystal Ball", "Inactive"
        )
        
    except Exception as e:
        return html.Div(f"Error loading data: {str(e)}", className='alert alert-error'), {'display': 'block'}
    
    # Build content
    content = []
    
    # Pivot Tables
    content.append(html.Details([
        html.Summary("📊 Pivot Tables", style={
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '600',
            'padding': '12px',
            'color': colors['text_primary']
        }),
        html.Div([
            create_pivot_table(pivot_data_regular, metrics, "📊 Plan Overview (Regular)", 
                              "inactive_pivot_regular", theme),
            create_pivot_table(pivot_data_crystal, metrics, "🔮 Plan Overview (Crystal Ball)", 
                              "inactive_pivot_crystal", theme)
        ], style={'padding': '16px'})
    ], open=True, style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["border"]}',
        'borderRadius': '8px',
        'marginBottom': '20px'
    }))
    
    # Charts
    charts = []
    subs_regular = all_regular_data.get("Subscriptions", {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
    subs_crystal = all_crystal_data.get("Subscriptions", {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
    
    for idx, chart_config in enumerate(CHART_METRICS):
        display_name = chart_config["display"]
        metric = chart_config["metric"]
        format_type = chart_config["format"]
        
        if format_type == "dollar":
            display_title = f"{display_name} ($)"
        elif format_type == "percent":
            display_title = f"{display_name} (%)"
        else:
            display_title = display_name
        
        chart_data_regular = all_regular_data.get(metric, {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
        chart_data_crystal = all_crystal_data.get(metric, {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
        
        charts.append(
            create_chart_pair_layout(
                chart_data_regular,
                chart_data_crystal,
                display_title,
                format_type,
                date_range=(from_date, to_date),
                chart_key=f"inactive_chart_{idx}",
                subscriptions_regular=subs_regular,
                subscriptions_crystal=subs_crystal,
                theme=theme
            )
        )
    
    content.append(html.Details([
        html.Summary("📈 Charts", style={
            'cursor': 'pointer',
            'fontSize': '16px',
            'fontWeight': '600',
            'padding': '12px',
            'color': colors['text_primary']
        }),
        html.Div(charts, style={'padding': '16px'})
    ], open=True, style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["border"]}',
        'borderRadius': '8px',
        'marginBottom': '20px'
    }))
    
    return html.Div(content), {'display': 'none'}


# Refresh BQ callback
@callback(
    Output('refresh-status', 'children'),
    Input('refresh-bq-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_bq_refresh(n_clicks):
    if not n_clicks:
        return no_update
    
    success, msg = refresh_bq_to_staging()
    if success:
        return html.Div(msg, className='alert alert-success')
    else:
        return html.Div(msg, className='alert alert-error')


# Refresh GCS callback
@callback(
    Output('refresh-status', 'children', allow_duplicate=True),
    Input('refresh-gcs-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_gcs_refresh(n_clicks):
    if not n_clicks:
        return no_update
    
    success, msg = refresh_gcs_from_staging()
    if success:
        return html.Div(msg, className='alert alert-success')
    else:
        return html.Div(msg, className='alert alert-error')
