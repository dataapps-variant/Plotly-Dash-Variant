"""
Authentication System for Variant Analytics Dashboard (Dash Version)
- Simple username/password auth
- Roles: admin (all access) and readonly (selected dashboards)
- Session management using Flask session
"""

from config import DEFAULT_USERS, DASHBOARDS, ROLE_DISPLAY

# In-memory user database (in production, use a proper database)
users_db = DEFAULT_USERS.copy()


def authenticate(username, password):
    """
    Authenticate user with username and password
    Returns user data if successful, None otherwise
    """
    if username in users_db:
        if users_db[username]["password"] == password:
            return {
                "username": username,
                "role": users_db[username]["role"],
                "name": users_db[username]["name"],
                "dashboards": users_db[username]["dashboards"]
            }
    return None


def is_admin(user):
    """Check if user is admin"""
    if user:
        return user.get("role") == "admin"
    return False


def can_access_dashboard(user, dashboard_id):
    """Check if user can access a specific dashboard"""
    if not user:
        return False
    
    # Check if dashboard is enabled
    dashboard = next((d for d in DASHBOARDS if d["id"] == dashboard_id), None)
    if not dashboard or not dashboard.get("enabled", False):
        return False
    
    # Admin has access to all
    if user["role"] == "admin" or user["dashboards"] == "all":
        return True
    
    return dashboard_id in user.get("dashboards", [])


def get_accessible_dashboards(user):
    """Get list of dashboards accessible to user"""
    if not user:
        return []
    
    if user["role"] == "admin" or user["dashboards"] == "all":
        return DASHBOARDS
    
    accessible = []
    for dashboard in DASHBOARDS:
        if dashboard["id"] in user.get("dashboards", []):
            accessible.append(dashboard)
    
    return accessible


def get_dashboard_access_for_user(username):
    """Get list of dashboard IDs a user has access to"""
    if username not in users_db:
        return []
    
    user_data = users_db[username]
    if user_data["role"] == "admin" or user_data["dashboards"] == "all":
        return "all"
    
    return user_data.get("dashboards", [])


def get_readonly_users_for_dashboard(dashboard_id):
    """Get list of readonly users who have access to a specific dashboard"""
    readonly_users = []
    for username, user_data in users_db.items():
        if user_data["role"] == "readonly":
            if user_data["dashboards"] == "all" or dashboard_id in user_data.get("dashboards", []):
                readonly_users.append(user_data["name"])
    
    return readonly_users


# =============================================================================
# ADMIN FUNCTIONS
# =============================================================================

def get_all_users():
    """Get all users (admin only)"""
    return users_db


def add_user(user_id, password, role, name, dashboards):
    """Add a new user (admin only)"""
    if user_id in users_db:
        return False, "User ID already exists"
    
    users_db[user_id] = {
        "password": password,
        "role": role,
        "name": name,
        "dashboards": dashboards if role == "readonly" else "all"
    }
    return True, "User created successfully"


def update_user(user_id, password=None, role=None, name=None, dashboards=None):
    """Update existing user (admin only)"""
    if user_id not in users_db:
        return False, "User not found"
    
    if password:
        users_db[user_id]["password"] = password
    if role:
        users_db[user_id]["role"] = role
        if role == "admin":
            users_db[user_id]["dashboards"] = "all"
    if name:
        users_db[user_id]["name"] = name
    if dashboards is not None and users_db[user_id]["role"] == "readonly":
        users_db[user_id]["dashboards"] = dashboards
    
    return True, "User updated successfully"


def delete_user(user_id, current_username):
    """Delete a user (admin only)"""
    if user_id not in users_db:
        return False, "User not found"
    
    if user_id == "admin":
        return False, "Cannot delete admin user"
    
    if user_id == current_username:
        return False, "Cannot delete yourself"
    
    del users_db[user_id]
    return True, "User deleted successfully"


def get_role_display(role):
    """Get display name for role"""
    return ROLE_DISPLAY.get(role, role)
