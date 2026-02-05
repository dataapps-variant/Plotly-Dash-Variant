"""
Theme System for Variant Analytics Dashboard - Plotly Dash Version
- Dark (default) and Light modes
- CSS generation for theming
"""

from config import THEME_COLORS


def get_theme_colors(theme="dark"):
    """Get the color palette for specified theme"""
    return THEME_COLORS.get(theme, THEME_COLORS["dark"])


def get_base_stylesheet(theme="dark"):
    """Generate base CSS stylesheet for the application"""
    colors = get_theme_colors(theme)
    
    return f"""
    /* Base Styles */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        box-sizing: border-box;
    }}
    
    body {{
        background-color: {colors['background']} !important;
        color: {colors['text_primary']} !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    .dash-loading {{
        background-color: {colors['background']} !important;
    }}
    
    /* Main container */
    #app-container {{
        background-color: {colors['background']};
        min-height: 100vh;
        padding: 20px 40px;
    }}
    
    /* Card styles */
    .card {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    
    /* Header styles */
    .header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }}
    
    .page-title {{
        font-size: 28px;
        font-weight: 700;
        color: {colors['text_primary']};
        text-align: center;
        margin: 0;
        padding: 10px 0;
    }}
    
    /* Filter section */
    .filter-container {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .filter-title {{
        font-size: 13px;
        font-weight: 600;
        color: {colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid {colors['border']};
    }}
    
    /* Button styles */
    .btn {{
        background: {colors['accent']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .btn:hover {{
        background: {colors['accent_hover']};
        box-shadow: 0 2px 8px rgba(20, 184, 166, 0.3);
    }}
    
    .btn-secondary {{
        background: {colors['surface']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
    }}
    
    .btn-secondary:hover {{
        background: {colors['hover']};
    }}
    
    /* Input styles */
    .dash-dropdown .Select-control {{
        background: {colors['input_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .dash-dropdown .Select-value-label,
    .dash-dropdown .Select-placeholder {{
        color: {colors['text_primary']} !important;
    }}
    
    .dash-dropdown .Select-menu-outer {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .dash-dropdown .Select-option {{
        background: {colors['card_bg']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    .dash-dropdown .Select-option:hover,
    .dash-dropdown .Select-option.is-focused {{
        background: {colors['hover']} !important;
    }}
    
    /* Date picker styles */
    .DateInput_input {{
        background: {colors['input_bg']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }}
    
    .SingleDatePickerInput {{
        background: {colors['input_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    /* Checklist styles */
    .checklist-container {{
        max-height: 180px;
        overflow-y: auto;
        padding: 10px;
        background: {colors['surface']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
    }}
    
    .checklist-container label {{
        display: block;
        padding: 4px 0;
        color: {colors['text_primary']};
        cursor: pointer;
    }}
    
    /* Tab styles */
    .tab-container {{
        display: flex;
        gap: 0;
        background: {colors['surface']};
        border-radius: 10px;
        padding: 4px;
        border: 1px solid {colors['border']};
        margin-bottom: 20px;
    }}
    
    .tab {{
        background: transparent;
        color: {colors['text_secondary']};
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .tab.active {{
        background: {colors['accent']};
        color: white;
    }}
    
    /* Table styles */
    .dash-table-container {{
        border-radius: 8px;
        overflow: hidden;
    }}
    
    .dash-spreadsheet-container .dash-spreadsheet-inner th {{
        background-color: {colors['table_header_bg']} !important;
        color: {colors['text_primary']} !important;
        font-weight: 600;
        border-bottom: 2px solid {colors['border']} !important;
    }}
    
    .dash-spreadsheet-container .dash-spreadsheet-inner td {{
        color: {colors['text_primary']} !important;
        border-right: 1px solid {colors['border']} !important;
        border-bottom: 1px solid {colors['border']} !important;
    }}
    
    .dash-spreadsheet-container .dash-spreadsheet-inner tr:nth-child(odd) {{
        background-color: {colors['table_row_odd']} !important;
    }}
    
    .dash-spreadsheet-container .dash-spreadsheet-inner tr:nth-child(even) {{
        background-color: {colors['table_row_even']} !important;
    }}
    
    /* Chart container */
    .chart-container {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    
    .chart-title {{
        font-size: 16px;
        font-weight: 600;
        color: {colors['text_primary']};
        margin-bottom: 12px;
    }}
    
    /* Legend box */
    .legend-box {{
        background: {colors['surface']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 16px;
        max-height: 60px;
        overflow-y: auto;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
    }}
    
    .legend-item {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        color: {colors['text_primary']};
    }}
    
    .legend-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }}
    
    /* Scrollbar styles */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['background']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['border']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['text_secondary']};
    }}
    
    /* Row and column utilities */
    .row {{
        display: flex;
        flex-wrap: wrap;
        margin: 0 -10px;
    }}
    
    .col {{
        padding: 0 10px;
    }}
    
    .col-2 {{ width: 16.66%; }}
    .col-3 {{ width: 25%; }}
    .col-4 {{ width: 33.33%; }}
    .col-6 {{ width: 50%; }}
    .col-12 {{ width: 100%; }}
    
    /* Spacing */
    .mb-1 {{ margin-bottom: 8px; }}
    .mb-2 {{ margin-bottom: 16px; }}
    .mb-3 {{ margin-bottom: 24px; }}
    .mt-1 {{ margin-top: 8px; }}
    .mt-2 {{ margin-top: 16px; }}
    .mt-3 {{ margin-top: 24px; }}
    
    /* Text utilities */
    .text-center {{ text-align: center; }}
    .text-right {{ text-align: right; }}
    .text-muted {{ color: {colors['text_secondary']}; }}
    
    /* Expander/Accordion styles */
    .expander {{
        background: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        margin-bottom: 16px;
    }}
    
    .expander-header {{
        padding: 12px 16px;
        cursor: pointer;
        font-weight: 500;
        color: {colors['text_primary']};
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .expander-content {{
        padding: 16px;
        border-top: 1px solid {colors['border']};
    }}
    
    /* Alert/Info boxes */
    .alert {{
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }}
    
    .alert-info {{
        background: rgba(20, 184, 166, 0.1);
        border: 1px solid {colors['accent']};
        color: {colors['accent']};
    }}
    
    .alert-warning {{
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid {colors['warning']};
        color: {colors['warning']};
    }}
    
    .alert-error {{
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid {colors['danger']};
        color: {colors['danger']};
    }}
    
    .alert-success {{
        background: rgba(52, 211, 153, 0.1);
        border: 1px solid {colors['success']};
        color: {colors['success']};
    }}
    """


def get_plotly_theme(theme="dark"):
    """Get Plotly theme configuration based on theme"""
    colors = get_theme_colors(theme)
    
    return {
        "paper_bgcolor": colors["card_bg"],
        "plot_bgcolor": colors["card_bg"],
        "font": {
            "family": "Inter, sans-serif",
            "size": 12,
            "color": colors["text_primary"]
        },
        "xaxis": {
            "gridcolor": colors["border"],
            "linecolor": colors["border"],
            "tickfont": {"color": colors["text_secondary"]},
            "title": {"font": {"color": colors["text_secondary"]}}
        },
        "yaxis": {
            "gridcolor": colors["border"],
            "linecolor": colors["border"],
            "tickfont": {"color": colors["text_secondary"]},
            "title": {"font": {"color": colors["text_secondary"]}}
        },
        "legend": {
            "font": {"color": colors["text_primary"]},
            "bgcolor": "rgba(0,0,0,0)"
        }
    }
