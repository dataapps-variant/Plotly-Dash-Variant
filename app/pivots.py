"""
Pivot Table Components for Variant Analytics Dashboard (Dash Version)
- Using Dash DataTable for AG Grid-like functionality
- CSV export
- Frozen columns
"""

import pandas as pd
from config import METRICS_CONFIG


def format_metric_value(value, metric_name, is_crystal_ball=False):
    """Format value based on metric type"""
    if value is None or pd.isna(value):
        return None
    
    config = METRICS_CONFIG.get(metric_name, {})
    format_type = config.get("format", "number")
    
    try:
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
    Process pivot data into DataFrame for DataTable
    
    Returns:
        DataFrame and list of date columns
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
    
    # Build rows
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
    
    # Column order
    column_order = ["App", "Plan", "Metric"] + date_columns
    df = df[[c for c in column_order if c in df.columns]]
    
    return df, date_columns


def get_datatable_columns(date_columns, theme="dark"):
    """Generate DataTable column definitions"""
    from theme import get_theme_colors
    colors = get_theme_colors(theme)
    
    columns = [
        {
            "name": "App",
            "id": "App",
            "type": "text",
        },
        {
            "name": "Plan",
            "id": "Plan",
            "type": "text",
        },
        {
            "name": "Metric",
            "id": "Metric",
            "type": "text",
        },
    ]
    
    for date_col in date_columns:
        columns.append({
            "name": date_col,
            "id": date_col,
            "type": "numeric",
            "format": {"specifier": ",.2f"}
        })
    
    return columns


def get_datatable_style(theme="dark"):
    """Get DataTable styling for given theme"""
    from theme import get_theme_colors
    colors = get_theme_colors(theme)
    
    style_table = {
        'overflowX': 'auto',
        'maxHeight': '500px',
        'overflowY': 'auto',
    }
    
    style_header = {
        'backgroundColor': colors['table_header_bg'],
        'color': colors['text_primary'],
        'fontWeight': '600',
        'fontSize': '12px',
        'borderBottom': f'2px solid {colors["border"]}',
        'textAlign': 'left',
        'padding': '10px 8px',
    }
    
    style_cell = {
        'backgroundColor': colors['card_bg'],
        'color': colors['text_primary'],
        'fontSize': '12px',
        'borderRight': f'1px solid {colors["border"]}',
        'borderBottom': f'1px solid {colors["border"]}',
        'padding': '8px',
        'textAlign': 'left',
        'minWidth': '80px',
        'maxWidth': '150px',
        'whiteSpace': 'normal',
    }
    
    style_data_conditional = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': colors['table_row_odd'],
        },
        {
            'if': {'row_index': 'even'},
            'backgroundColor': colors['table_row_even'],
        },
        {
            'if': {'column_id': 'App'},
            'width': '80px',
            'minWidth': '80px',
            'maxWidth': '100px',
        },
        {
            'if': {'column_id': 'Plan'},
            'width': '130px',
            'minWidth': '130px',
            'maxWidth': '150px',
        },
        {
            'if': {'column_id': 'Metric'},
            'width': '200px',
            'minWidth': '200px',
            'maxWidth': '220px',
        },
    ]
    
    # Right-align numeric columns (date columns)
    style_data_conditional.append({
        'if': {'column_type': 'numeric'},
        'textAlign': 'right',
    })
    
    return {
        'style_table': style_table,
        'style_header': style_header,
        'style_cell': style_cell,
        'style_data_conditional': style_data_conditional,
    }
