"""
Theme System for Variant Analytics Dashboard (Dash Version)
- Full screen layout
- Dark (default) and Light modes
- CSS generation for Dash
"""

from config import THEME_COLORS


def get_theme_colors(theme="dark"):
    """Get the color palette for specified theme"""
    return THEME_COLORS.get(theme, THEME_COLORS["dark"])


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


def generate_css(theme="dark"):
    """Generate CSS for the application based on theme"""
    colors = get_theme_colors(theme)
    
    return f"""
    /* FULL SCREEN LAYOUT */
    html, body {{
        background-color: {colors['background']} !important;
        color: {colors['text_primary']} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        margin: 0 !important;
        padding: 0 !important;
        min-height: 100vh;
    }}
    
    #root, ._dash-loading {{
        background-color: {colors['background']} !important;
    }}
    
    .dash-container {{
        background-color: {colors['background']} !important;
        min-height: 100vh;
        padding: 1rem 2rem;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {colors['text_primary']} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    p, span, label, div {{
        color: {colors['text_primary']};
    }}
    
    .card {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }}
    
    .filter-title {{
        font-size: 13px !important;
        font-weight: 600 !important;
        color: {colors['text_secondary']} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 10px !important;
        padding-bottom: 8px !important;
        border-bottom: 1px solid {colors['border']} !important;
    }}
    
    /* Buttons */
    .btn-primary {{
        background: {colors['accent']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        cursor: pointer;
        transition: all 0.2s ease !important;
    }}
    
    .btn-primary:hover {{
        background: {colors['accent_hover']} !important;
        box-shadow: 0 2px 8px rgba(20, 184, 166, 0.3) !important;
    }}
    
    .btn-secondary {{
        background: {colors['surface']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        cursor: pointer;
    }}
    
    /* Inputs */
    input, select, .Select-control {{
        background: {colors['input_bg']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    input:focus, select:focus {{
        border-color: {colors['accent']} !important;
        box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.2) !important;
    }}
    
    /* Dash Core Components Styling */
    .Select-menu-outer {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
    }}
    
    .Select-option {{
        background: {colors['card_bg']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    .Select-option:hover {{
        background: {colors['hover']} !important;
    }}
    
    .Select-value-label {{
        color: {colors['text_primary']} !important;
    }}
    
    .Select-placeholder {{
        color: {colors['text_secondary']} !important;
    }}
    
    /* Tabs */
    .tab-container {{
        background: {colors['surface']} !important;
        border-radius: 10px !important;
        padding: 4px !important;
        border: 1px solid {colors['border']} !important;
        display: inline-flex;
        gap: 4px;
    }}
    
    .tab {{
        background: transparent !important;
        color: {colors['text_secondary']} !important;
        border-radius: 8px !important;
        padding: 8px 24px !important;
        font-weight: 500 !important;
        border: none !important;
        cursor: pointer;
    }}
    
    .tab--selected {{
        background: {colors['accent']} !important;
        color: white !important;
    }}
    
    /* DataTable / AG Grid */
    .dash-table-container {{
        border-radius: 8px !important;
        border: 1px solid {colors['border']} !important;
        overflow: hidden;
    }}
    
    .dash-header {{
        background-color: {colors['table_header_bg']} !important;
        color: {colors['text_primary']} !important;
        font-weight: 600 !important;
        border-bottom: 2px solid {colors['border']} !important;
    }}
    
    .dash-cell {{
        color: {colors['text_primary']} !important;
        border-right: 1px solid {colors['border']} !important;
        border-bottom: 1px solid {colors['border']} !important;
    }}
    
    .dash-table-container .row-0, 
    .dash-table-container .row-2,
    .dash-table-container .row-4 {{
        background-color: {colors['table_row_even']} !important;
    }}
    
    .dash-table-container .row-1,
    .dash-table-container .row-3,
    .dash-table-container .row-5 {{
        background-color: {colors['table_row_odd']} !important;
    }}
    
    /* Expander / Collapsible */
    .collapse-header {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        color: {colors['text_primary']} !important;
        font-weight: 500 !important;
        padding: 12px 16px;
        cursor: pointer;
    }}
    
    .collapse-content {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 16px;
    }}
    
    /* Scrollbars */
    ::-webkit-scrollbar {{
        width: 8px !important;
        height: 8px !important;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['background']} !important;
        border-radius: 4px !important;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['border']} !important;
        border-radius: 4px !important;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['text_secondary']} !important;
    }}
    
    /* Checkbox */
    .checkbox-container {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }}
    
    .checkbox-container input[type="checkbox"] {{
        width: 16px;
        height: 16px;
        accent-color: {colors['accent']};
    }}
    
    /* Alert/Info boxes */
    .alert {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        padding: 12px 16px;
    }}
    
    .alert-info {{
        border-left: 4px solid {colors['accent']} !important;
    }}
    
    .alert-success {{
        border-left: 4px solid {colors['success']} !important;
    }}
    
    .alert-warning {{
        border-left: 4px solid {colors['warning']} !important;
    }}
    
    .alert-danger {{
        border-left: 4px solid {colors['danger']} !important;
    }}
    
    /* Logo Header */
    .logo-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px 0;
        text-align: center;
    }}
    
    .logo-header .logo {{
        width: 80px;
        height: 80px;
        background: {colors['accent']};
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        font-weight: bold;
        color: white;
    }}
    
    .logo-header .title {{
        font-size: 28px;
        font-weight: 700;
        color: {colors['text_primary']};
        margin: 16px 0 0 0;
        letter-spacing: 3px;
    }}
    
    .logo-header .subtitle {{
        font-size: 16px;
        color: {colors['text_secondary']};
        margin: 8px 0 0 0;
        font-weight: 400;
    }}
    
    /* Legend */
    .legend-container {{
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
    
    .legend-color {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }}
    
    /* Menu Popover */
    .menu-popover {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        padding: 8px;
    }}
    
    .menu-item {{
        padding: 8px 16px;
        cursor: pointer;
        border-radius: 4px;
        color: {colors['text_primary']};
    }}
    
    .menu-item:hover {{
        background: {colors['hover']};
    }}
    
    /* Dropdown */
    .dropdown {{
        position: relative;
        display: inline-block;
    }}
    
    .dropdown-content {{
        display: none;
        position: absolute;
        right: 0;
        background: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        min-width: 160px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
    }}
    
    .dropdown:hover .dropdown-content {{
        display: block;
    }}
    """
