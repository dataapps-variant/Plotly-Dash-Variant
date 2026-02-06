"""
Color System for Variant Analytics Dashboard (Dash Version)
- App-based colors (14 apps)
- Shade generation for multiple plans per app
- Color map building for charts
"""

from config import APP_COLORS


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2])))
    )


def lighten_color(hex_color, factor=0.2):
    """Lighten a hex color by a factor (0-1)"""
    rgb = hex_to_rgb(hex_color)
    new_rgb = tuple(c + (255 - c) * factor for c in rgb)
    return rgb_to_hex(new_rgb)


def darken_color(hex_color, factor=0.2):
    """Darken a hex color by a factor (0-1)"""
    rgb = hex_to_rgb(hex_color)
    new_rgb = tuple(c * (1 - factor) for c in rgb)
    return rgb_to_hex(new_rgb)


def get_app_from_plan(plan_name):
    """
    Extract App name from Plan name
    Handles special cases like CT-Non-JP and CT-JP
    """
    if plan_name is None:
        return "Unknown"
    
    plan_upper = plan_name.upper()
    
    # Check for special CT cases first
    if "CT" in plan_upper:
        if "NON-JP" in plan_upper or "NONJP" in plan_upper:
            return "CT-Non-JP"
        elif "JP" in plan_upper and "NON" not in plan_upper:
            return "CT-JP"
        if plan_name.startswith("CT"):
            return "CT-Non-JP"
    
    # Extract first 2 characters as App prefix
    if len(plan_name) >= 2:
        prefix = plan_name[:2].upper()
        if prefix in APP_COLORS:
            return prefix
    
    return "Unknown"


def get_plan_color(plan_name, plan_index_in_app=0):
    """
    Get color for a specific plan based on its App and position
    """
    app_name = get_app_from_plan(plan_name)
    base_color = APP_COLORS.get(app_name, "#6B7280")
    
    shade_pattern = [
        0,
        -0.35,
        0.35,
        -0.55,
        0.55,
        -0.25,
        0.25,
        -0.45,
        0.45,
        -0.15,
    ]
    
    shade_index = plan_index_in_app % len(shade_pattern)
    shade_value = shade_pattern[shade_index]
    
    if shade_value > 0:
        return lighten_color(base_color, shade_value)
    elif shade_value < 0:
        return darken_color(base_color, abs(shade_value))
    else:
        return base_color


def build_plan_color_map(plans):
    """
    Build a color map for a list of plans
    Groups plans by App and assigns shades
    """
    app_plans = {}
    for plan in plans:
        app = get_app_from_plan(plan)
        if app not in app_plans:
            app_plans[app] = []
        app_plans[app].append(plan)
    
    for app in app_plans:
        app_plans[app].sort()
    
    color_map = {}
    for app, plan_list in app_plans.items():
        for idx, plan in enumerate(plan_list):
            color_map[plan] = get_plan_color(plan, idx)
    
    return color_map


def get_chart_colors(plans):
    """
    Get ordered list of colors for a list of plans (for Plotly charts)
    """
    color_map = build_plan_color_map(plans)
    return [color_map.get(plan, "#6B7280") for plan in plans]


FALLBACK_COLORS = [
    "#6B7280",
    "#9CA3AF",
    "#4B5563",
    "#D1D5DB",
    "#374151",
]


def get_fallback_color(index):
    """Get a fallback color by index"""
    return FALLBACK_COLORS[index % len(FALLBACK_COLORS)]
