"""
Pivot Table Components for Variant Analytics Dashboard - Plotly Dash Version

Using Dash DataTable instead of AG Grid
"""

import pandas as pd
from dash import html, dash_table, dcc
from config import METRICS_CONFIG
from theme import get_theme_colors


def format_metric_value(value, metric_name, is_crystal_ball=False):
    """Format value based on metric type - rounded to 2 decimal places"""
    if value is None or pd.isna(value):
        return None
    
    config = METRICS_CONFIG.get(metric_name, {})
    format_type = config.get("format", "number")
    
    try:
        # Special case: Rebills in Crystal Ball = no decimals
        if metric_name == "Rebills" and is_crystal_ball:
            return round(float(value))
        
        if format_type == "percent":
            return round(float(value) * 100, 2)
        return round(float(value), 2)
    except:
        return None


def get_display_metric_name(metric_name):
    """Get display name with suffix"""
    config = METRICS_CONFIG.get(metric_name, {})
    display = config.get("display", metric_name)
    suffix = config.get("suffix", "")
    return f"{display}{suffix}"


def process_pivot_data(pivot_data, selected_metrics, is_crystal_ball=False):
    """
    Process pivot data into DataFrame for Dash DataTable
    """
    
    if not pivot_data or "Reporting_Date" not in pivot_data or len(pivot_data["Reporting_Date"]) == 0:
        return None, []
    
    # Get unique dates sorted newest first
    unique_dates = sorted(set(pivot_data["Reporting_Date"]), reverse=True)
    
    # Format dates as MM/DD/YYYY for column headers
    date_columns = []
    date_map = {}
    for d in unique_dates:
        if hasattr(d, 'strftime'):
            formatted = d.strftime("%m/%d/%Y")
        else:
            formatted = str(d)
        date_columns.append(formatted)
        date_map[d] = formatted
    
    # Get unique App_Name + Plan_Name combinations
    plan_combos = []
    seen = set()
    for i in range(len(pivot_data["App_Name"])):
        combo = (pivot_data["App_Name"][i], pivot_data["Plan_Name"][i])
        if combo not in seen:
            plan_combos.append(combo)
            seen.add(combo)
    
    plan_combos.sort(key=lambda x: (x[0], x[1]))
    
    # Build lookup dictionary
    lookup = {}
    for i in range(len(pivot_data["Reporting_Date"])):
        app = pivot_data["App_Name"][i]
        plan = pivot_data["Plan_Name"][i]
        date = pivot_data["Reporting_Date"][i]
        
        key = (app, plan, date)
        if key not in lookup:
            lookup[key] = {}
        
        for metric in selected_metrics:
            if metric in pivot_data:
                lookup[key][metric] = pivot_data[metric][i]
    
    # Build rows for DataFrame
    rows = []
    for app_name, plan_name in plan_combos:
        for metric in selected_metrics:
            row = {
                "App": app_name,
                "Plan": plan_name,
                "Metric": get_display_metric_name(metric),
            }
            
            for date in unique_dates:
                formatted_date = date_map[date]
                key = (app_name, plan_name, date)
                raw_value = lookup.get(key, {}).get(metric, None)
                formatted_value = format_metric_value(raw_value, metric, is_crystal_ball)
                row[formatted_date] = formatted_value
            
            rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Column order: App, Plan, Metric, then date columns
    column_order = ["App", "Plan", "Metric"] + date_columns
    df = df[[c for c in column_order if c in df.columns]]
    
    return df, date_columns


def create_pivot_table(pivot_data, selected_metrics, title, table_id="pivot", theme="dark"):
    """
    Create a Dash DataTable component for pivot table
    """
    
    colors = get_theme_colors(theme)
    
    # Check if this is Crystal Ball table
    is_crystal_ball = "crystal" in table_id.lower() or "crystal ball" in title.lower()
    
    # Process data
    df, date_columns = process_pivot_data(pivot_data, selected_metrics, is_crystal_ball)
    
    if df is None or df.empty:
        return html.Div([
            html.H4(title, style={'color': colors['text_primary']}),
            html.Div("No data available for selected filters.", 
                    className='alert alert-info')
        ])
    
    # Generate CSV data for download
    csv_string = df.to_csv(index=False, encoding='utf-8')
    clean_title = title.replace('📊', '').replace('🔮', '').strip().replace(' ', '_')
    
    # Define columns for DataTable
    columns = []
    for col in df.columns:
        col_def = {"name": col, "id": col}
        if col in date_columns:
            col_def["type"] = "numeric"
            col_def["format"] = {"specifier": ",.2f"}
        columns.append(col_def)
    
    # Style conditions for alternating rows
    style_data_conditional = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': colors['table_row_odd']
        },
        {
            'if': {'row_index': 'even'},
            'backgroundColor': colors['table_row_even']
        }
    ]
    
    # Add right alignment for date columns
    for date_col in date_columns:
        style_data_conditional.append({
            'if': {'column_id': date_col},
            'textAlign': 'right'
        })
    
    return html.Div([
        # Header with title and download button
        html.Div([
            html.H4(title, style={
                'color': colors['text_primary'],
                'margin': '0',
                'flex': '1'
            }),
            html.A(
                html.Button("📥 Download CSV", className='btn btn-secondary', style={
                    'fontSize': '12px',
                    'padding': '6px 12px'
                }),
                href=f"data:text/csv;charset=utf-8,{csv_string}",
                download=f"{clean_title}.csv"
            )
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '16px'
        }),
        
        # DataTable
        dash_table.DataTable(
            id=table_id,
            columns=columns,
            data=df.to_dict('records'),
            page_size=50,
            
            # Styling
            style_table={
                'overflowX': 'auto',
                'borderRadius': '8px',
                'border': f'1px solid {colors["border"]}'
            },
            style_header={
                'backgroundColor': colors['table_header_bg'],
                'color': colors['text_primary'],
                'fontWeight': '600',
                'fontSize': '12px',
                'borderBottom': f'2px solid {colors["border"]}',
                'textAlign': 'left',
                'padding': '10px 8px'
            },
            style_cell={
                'backgroundColor': colors['card_bg'],
                'color': colors['text_primary'],
                'fontSize': '12px',
                'padding': '8px',
                'border': f'1px solid {colors["border"]}',
                'textAlign': 'left',
                'minWidth': '80px',
                'maxWidth': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis'
            },
            style_data_conditional=style_data_conditional,
            
            # Fixed columns (App, Plan, Metric)
            fixed_columns={'headers': True, 'data': 3},
            
            # Enable filtering and sorting
            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            
            # Row selection
            row_selectable=False,
            
            # Export
            export_format='csv'
        )
    ], style={
        'marginBottom': '24px'
    })
