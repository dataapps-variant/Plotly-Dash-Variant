"""
ICARUS - Plan (Historical) Dashboard Page for Variant Analytics Dashboard (Dash Version)
"""

from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import plotly.graph_objects as go
from theme import get_theme_colors
from config import BC_OPTIONS, COHORT_OPTIONS, DEFAULT_BC, DEFAULT_COHORT, DEFAULT_PLAN, CHART_METRICS, METRICS_CONFIG
from colors import build_plan_color_map
from charts import build_line_chart, build_legend_html
from pivots import process_pivot_data, get_datatable_columns, get_datatable_style


def get_plans_by_app(plan_groups):
    """Group plans by App_Name"""
    result = {}
    for app, plan in zip(plan_groups["App_Name"], plan_groups["Plan_Name"]):
        if app not in result:
            result[app] = []
        if plan not in result[app]:
            result[app].append(plan)
    return result


def create_filter_section(plan_groups, min_date, max_date, colors, prefix=""):
    """Create the filters section"""
    plans_by_app = get_plans_by_app(plan_groups)
    app_names = sorted(plans_by_app.keys())
    
    # Build plan options for dropdown
    plan_options = []
    for app in app_names:
        for plan in sorted(plans_by_app[app]):
            plan_options.append({'label': f'{app} - {plan}', 'value': plan})
    
    # Build metrics options
    metrics_options = [
        {'label': METRICS_CONFIG[m]['display'], 'value': m}
        for m in METRICS_CONFIG.keys()
    ]
    
    return html.Div([
        html.Details([
            html.Summary('📊 Filters', style={
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'padding': '12px 16px',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderRadius': '8px',
            }),
            html.Div([
                # Row 1: Date Range, BC, Cohort, Reset
                html.Div([
                    html.Div([
                        html.Div('DATE RANGE', className='filter-title'),
                        html.Div([
                            dcc.DatePickerSingle(
                                id=f'{prefix}from-date',
                                date=min_date,
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                display_format='YYYY-MM-DD',
                                style={'marginRight': '8px'}
                            ),
                            html.Span(' to ', style={'color': colors['text_secondary']}),
                            dcc.DatePickerSingle(
                                id=f'{prefix}to-date',
                                date=max_date,
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                display_format='YYYY-MM-DD',
                                style={'marginLeft': '8px'}
                            ),
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                    ], style={'flex': '2', 'marginRight': '16px'}),
                    
                    html.Div([
                        html.Div('BILLING CYCLE', className='filter-title'),
                        dcc.Dropdown(
                            id=f'{prefix}bc-select',
                            options=[{'label': str(bc), 'value': bc} for bc in BC_OPTIONS],
                            value=DEFAULT_BC,
                            clearable=False,
                            style={'width': '100%'}
                        ),
                    ], style={'flex': '1', 'marginRight': '16px'}),
                    
                    html.Div([
                        html.Div('COHORT', className='filter-title'),
                        dcc.Dropdown(
                            id=f'{prefix}cohort-select',
                            options=[{'label': c, 'value': c} for c in COHORT_OPTIONS],
                            value=DEFAULT_COHORT,
                            clearable=False,
                            style={'width': '100%'}
                        ),
                    ], style={'flex': '1', 'marginRight': '16px'}),
                    
                    html.Div([
                        html.Div(' ', className='filter-title'),
                        html.Button('🔄 Reset', id=f'{prefix}reset-btn', className='btn-secondary',
                                   style={'width': '100%', 'padding': '8px 16px'}),
                    ], style={'flex': '1'}),
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Row 2: Plans and Metrics
                html.Div([
                    html.Div([
                        html.Div('PLAN GROUPS', className='filter-title'),
                        dcc.Dropdown(
                            id=f'{prefix}plans-select',
                            options=plan_options,
                            value=[DEFAULT_PLAN] if DEFAULT_PLAN in [p['value'] for p in plan_options] else [],
                            multi=True,
                            placeholder='Select plans...',
                            style={'width': '100%'}
                        ),
                    ], style={'flex': '4', 'marginRight': '16px'}),
                    
                    html.Div([
                        html.Div('METRICS', className='filter-title'),
                        dcc.Dropdown(
                            id=f'{prefix}metrics-select',
                            options=metrics_options,
                            value=list(METRICS_CONFIG.keys()),
                            multi=True,
                            placeholder='Select metrics...',
                            style={'width': '100%'}
                        ),
                    ], style={'flex': '1'}),
                ], style={'display': 'flex', 'marginBottom': '20px'}),
                
                # Apply button
                html.Div([
                    html.Button('✅ Apply Filter', id=f'{prefix}apply-btn', className='btn-primary',
                               style={'padding': '10px 24px', 'fontSize': '14px'}),
                ], style={'display': 'flex', 'justifyContent': 'flex-end'}),
                
            ], style={
                'padding': '20px',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderTop': 'none',
                'borderRadius': '0 0 8px 8px',
            }),
        ], open=True),
    ])


def create_pivot_section(colors, prefix=""):
    """Create the pivot tables section placeholder"""
    return html.Div([
        html.Details([
            html.Summary('📊 Pivot Tables', style={
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'padding': '12px 16px',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderRadius': '8px',
            }),
            html.Div([
                # Regular Pivot Table
                html.H4('📊 Plan Overview (Regular)', style={
                    'color': colors['text_primary'],
                    'marginBottom': '16px',
                }),
                html.Div(id=f'{prefix}pivot-regular'),
                
                html.Br(),
                
                # Crystal Ball Pivot Table
                html.H4('🔮 Plan Overview (Crystal Ball)', style={
                    'color': colors['text_primary'],
                    'marginBottom': '16px',
                }),
                html.Div(id=f'{prefix}pivot-crystal'),
                
            ], style={
                'padding': '20px',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderTop': 'none',
                'borderRadius': '0 0 8px 8px',
            }),
        ], open=True),
    ], style={'marginTop': '20px'})


def create_charts_section(colors, prefix=""):
    """Create the charts section placeholder"""
    return html.Div([
        html.Details([
            html.Summary('📈 Charts', style={
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '600',
                'color': colors['text_primary'],
                'padding': '12px 16px',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderRadius': '8px',
            }),
            html.Div(id=f'{prefix}charts-container', style={
                'padding': '20px',
                'background': colors['card_bg'],
                'border': f'1px solid {colors["border"]}',
                'borderTop': 'none',
                'borderRadius': '0 0 8px 8px',
            }),
        ], open=True),
    ], style={'marginTop': '20px'})


def create_icarus_layout(user, theme='dark'):
    """Create the ICARUS Historical dashboard layout"""
    from bigquery_client import load_date_bounds, load_plan_groups, get_cache_info
    
    colors = get_theme_colors(theme)
    theme_icon = "☀️" if theme == "dark" else "🌙"
    
    # Load initial data
    try:
        date_bounds = load_date_bounds()
        min_date = date_bounds["min_date"]
        max_date = date_bounds["max_date"]
    except Exception as e:
        min_date = None
        max_date = None
    
    try:
        plan_groups_active = load_plan_groups("Active")
    except:
        plan_groups_active = {"App_Name": [], "Plan_Name": []}
    
    try:
        plan_groups_inactive = load_plan_groups("Inactive")
    except:
        plan_groups_inactive = {"App_Name": [], "Plan_Name": []}
    
    cache_info = get_cache_info()
    
    return html.Div([
        # Store for current theme
        dcc.Store(id='icarus-theme', data=theme),
        
        # Header row
        html.Div([
            dcc.Link('← Back', href='/', className='btn-secondary',
                    style={'textDecoration': 'none', 'padding': '8px 16px'}),
            html.H1('ICARUS - Plan (Historical)', style={
                'fontSize': '28px',
                'fontWeight': '700',
                'color': colors['text_primary'],
                'margin': '0',
                'textAlign': 'center',
                'flex': '1',
            }),
            html.Div([
                html.Button(theme_icon, id='theme-toggle', className='btn-secondary',
                           style={'marginRight': '8px'}),
                html.Button('Logout', id='logout-button', className='btn-secondary'),
            ]),
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'padding': '16px 0',
            'borderBottom': f'1px solid {colors["border"]}',
        }),
        
        # Refresh section
        html.Div([
            html.Div([
                html.Button('🔄', id='refresh-bq-btn', className='btn-secondary',
                           style={'marginRight': '8px', 'padding': '4px 8px'}),
                html.Span(f'BQ: {cache_info.get("last_bq_refresh", "--")}', style={
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'color': colors['text_primary'],
                }),
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                html.Span(f'GCS: {cache_info.get("last_gcs_refresh", "--")}', style={
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'color': colors['text_primary'],
                }),
                html.Button('🔄', id='refresh-gcs-btn', className='btn-secondary',
                           style={'marginLeft': '8px', 'padding': '4px 8px'}),
            ], style={'display': 'flex', 'alignItems': 'center'}),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'padding': '16px 0',
        }),
        
        html.Div(id='refresh-message'),
        
        # Tabs for Active/Inactive
        dcc.Tabs(id='active-inactive-tabs', value='active', children=[
            dcc.Tab(label='📈 Active', value='active', className='tab', selected_className='tab--selected'),
            dcc.Tab(label='📉 Inactive', value='inactive', className='tab', selected_className='tab--selected'),
        ], className='tab-container'),
        
        html.Br(),
        
        # Active Tab Content
        html.Div([
            create_filter_section(plan_groups_active, min_date, max_date, colors, 'active-') if min_date else html.Div('Error loading data'),
            create_pivot_section(colors, 'active-'),
            create_charts_section(colors, 'active-'),
        ], id='active-content', style={'display': 'block'}),
        
        # Inactive Tab Content
        html.Div([
            create_filter_section(plan_groups_inactive, min_date, max_date, colors, 'inactive-') if min_date else html.Div('Error loading data'),
            create_pivot_section(colors, 'inactive-'),
            create_charts_section(colors, 'inactive-'),
        ], id='inactive-content', style={'display': 'none'}),
        
    ], style={
        'minHeight': '100vh',
        'background': colors['background'],
        'padding': '0 20px',
    })


# =============================================================================
# CALLBACKS FOR ICARUS PAGE
# =============================================================================

def register_icarus_callbacks(app):
    """Register callbacks for the ICARUS page"""
    
    # Tab switching
    @app.callback(
        [Output('active-content', 'style'), Output('inactive-content', 'style')],
        [Input('active-inactive-tabs', 'value')]
    )
    def switch_tabs(tab):
        if tab == 'active':
            return {'display': 'block'}, {'display': 'none'}
        else:
            return {'display': 'none'}, {'display': 'block'}
    
    # Active tab: Apply filters and update pivots
    @app.callback(
        [Output('active-pivot-regular', 'children'),
         Output('active-pivot-crystal', 'children'),
         Output('active-charts-container', 'children')],
        [Input('active-apply-btn', 'n_clicks')],
        [State('active-from-date', 'date'),
         State('active-to-date', 'date'),
         State('active-bc-select', 'value'),
         State('active-cohort-select', 'value'),
         State('active-plans-select', 'value'),
         State('active-metrics-select', 'value'),
         State('icarus-theme', 'data')],
        prevent_initial_call=True
    )
    def update_active_content(n_clicks, from_date, to_date, bc, cohort, plans, metrics, theme):
        return update_dashboard_content(
            from_date, to_date, bc, cohort, plans, metrics, 
            'Active', theme or 'dark'
        )
    
    # Inactive tab: Apply filters and update pivots
    @app.callback(
        [Output('inactive-pivot-regular', 'children'),
         Output('inactive-pivot-crystal', 'children'),
         Output('inactive-charts-container', 'children')],
        [Input('inactive-apply-btn', 'n_clicks')],
        [State('inactive-from-date', 'date'),
         State('inactive-to-date', 'date'),
         State('inactive-bc-select', 'value'),
         State('inactive-cohort-select', 'value'),
         State('inactive-plans-select', 'value'),
         State('inactive-metrics-select', 'value'),
         State('icarus-theme', 'data')],
        prevent_initial_call=True
    )
    def update_inactive_content(n_clicks, from_date, to_date, bc, cohort, plans, metrics, theme):
        return update_dashboard_content(
            from_date, to_date, bc, cohort, plans, metrics,
            'Inactive', theme or 'dark'
        )
    
    # BQ Refresh
    @app.callback(
        Output('refresh-message', 'children'),
        [Input('refresh-bq-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_bq_refresh(n_clicks):
        from bigquery_client import refresh_bq_to_staging
        if n_clicks:
            success, msg = refresh_bq_to_staging()
            colors = get_theme_colors('dark')
            if success:
                return html.Div(msg, className='alert alert-success')
            else:
                return html.Div(msg, className='alert alert-danger')
        return no_update
    
    # GCS Refresh
    @app.callback(
        Output('refresh-message', 'children', allow_duplicate=True),
        [Input('refresh-gcs-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_gcs_refresh(n_clicks):
        from bigquery_client import refresh_gcs_from_staging
        if n_clicks:
            success, msg = refresh_gcs_from_staging()
            if success:
                return html.Div(msg, className='alert alert-success')
            else:
                return html.Div(msg, className='alert alert-danger')
        return no_update


def update_dashboard_content(from_date, to_date, bc, cohort, plans, metrics, active_inactive, theme):
    """Update dashboard content with new filter values"""
    from bigquery_client import load_pivot_data, load_all_chart_data
    
    colors = get_theme_colors(theme)
    
    # Validation
    if not plans:
        msg = html.Div('⚠️ Please select at least one Plan.', className='alert alert-warning')
        return msg, msg, msg
    
    if not metrics:
        msg = html.Div('⚠️ Please select at least one Metric.', className='alert alert-warning')
        return msg, msg, msg
    
    try:
        # Load pivot data
        pivot_regular = load_pivot_data(
            from_date, to_date, bc, cohort, plans, metrics, 'Regular', active_inactive
        )
        pivot_crystal = load_pivot_data(
            from_date, to_date, bc, cohort, plans, metrics, 'Crystal Ball', active_inactive
        )
        
        # Process pivot data
        df_regular, date_cols_regular = process_pivot_data(pivot_regular, metrics, False)
        df_crystal, date_cols_crystal = process_pivot_data(pivot_crystal, metrics, True)
        
        # Get datatable styling
        table_style = get_datatable_style(theme)
        
        # Create pivot tables
        if df_regular is not None and not df_regular.empty:
            pivot_regular_component = dash_table.DataTable(
                data=df_regular.to_dict('records'),
                columns=get_datatable_columns(date_cols_regular, theme),
                fixed_columns={'headers': True, 'data': 3},
                export_format='csv',
                **table_style
            )
        else:
            pivot_regular_component = html.Div('No data available', style={'color': colors['text_secondary']})
        
        if df_crystal is not None and not df_crystal.empty:
            pivot_crystal_component = dash_table.DataTable(
                data=df_crystal.to_dict('records'),
                columns=get_datatable_columns(date_cols_crystal, theme),
                fixed_columns={'headers': True, 'data': 3},
                export_format='csv',
                **table_style
            )
        else:
            pivot_crystal_component = html.Div('No data available', style={'color': colors['text_secondary']})
        
        # Load chart data
        chart_metric_names = [cm["metric"] for cm in CHART_METRICS]
        if "Subscriptions" not in chart_metric_names:
            chart_metric_names.append("Subscriptions")
        
        all_regular_data = load_all_chart_data(
            from_date, to_date, bc, cohort, plans, chart_metric_names, 'Regular', active_inactive
        )
        all_crystal_data = load_all_chart_data(
            from_date, to_date, bc, cohort, plans, chart_metric_names, 'Crystal Ball', active_inactive
        )
        
        subs_regular = all_regular_data.get("Subscriptions", {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
        subs_crystal = all_crystal_data.get("Subscriptions", {"Plan_Name": [], "Reporting_Date": [], "metric_value": []})
        
        # Create charts
        chart_components = []
        date_range = (from_date, to_date)
        
        for chart_config in CHART_METRICS:
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
            
            is_subscriptions_chart = "Subscriptions" in display_name
            
            fig_regular, plans_regular = build_line_chart(
                chart_data_regular, display_title, format_type, date_range,
                subs_regular, is_subscriptions_chart, theme
            )
            fig_crystal, plans_crystal = build_line_chart(
                chart_data_crystal, f"{display_title} (Crystal Ball)", format_type, date_range,
                subs_crystal, is_subscriptions_chart, theme
            )
            
            # Build legend
            if plans_regular:
                color_map = build_plan_color_map(plans_regular)
                legend_html = build_legend_html(plans_regular, color_map, theme)
            else:
                legend_html = ""
            
            chart_components.append(
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4(display_title, style={'color': colors['text_primary'], 'marginBottom': '8px'}),
                            html.Div(
                                children=[html.Span(legend_html)] if legend_html else [],
                                className='legend-container'
                            ) if legend_html else None,
                            dcc.Graph(figure=fig_regular, config={'displayModeBar': True, 'displaylogo': False}),
                        ], style={'flex': '1', 'marginRight': '16px'}),
                        html.Div([
                            html.H4(f"{display_title} (Crystal Ball)", style={'color': colors['text_primary'], 'marginBottom': '8px'}),
                            html.Div(
                                children=[html.Span(legend_html)] if legend_html else [],
                                className='legend-container'
                            ) if legend_html else None,
                            dcc.Graph(figure=fig_crystal, config={'displayModeBar': True, 'displaylogo': False}),
                        ], style={'flex': '1'}),
                    ], style={'display': 'flex'}),
                ], style={'marginBottom': '24px'})
            )
        
        charts_container = html.Div(chart_components)
        
        return pivot_regular_component, pivot_crystal_component, charts_container
        
    except Exception as e:
        error_msg = html.Div(f'Error: {str(e)}', className='alert alert-danger')
        return error_msg, error_msg, error_msg
