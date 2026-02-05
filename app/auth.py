"""
Authentication System for Variant Analytics Dashboard - Plotly Dash Version
- Simple username/password auth using Flask session
- Roles: admin (all access) and readonly (selected dashboards)
"""

from flask import session
from config import DEFAULT_USERS, DASHBOARDS, ROLE_DISPLAY

# In-memory user database (would be replaced with real DB in production)
_users_db = None


def get_users_db():
    """Get or initialize the users database"""
    global _users_db
    if _users_db is None:
        _users_db = DEFAULT_USERS.copy()
    return _users_db


def authenticate(username, password):
    """
    Authenticate user with username and password
    Returns True if successful, False otherwise
    """
    users = get_users_db()
    
    if username in users:
        if users[username]["password"] == password:
            session['authenticated'] = True
            session['user'] = {
                "username": username,
                "role": users[username]["role"],
                "name": users[username]["name"],
                "dashboards": users[username]["dashboards"]
            }
            return True
    return False


def logout():
    """Log out current user"""
    session.pop('authenticated', None)
    session.pop('user', None)


def is_authenticated():
    """Check if user is authenticated"""
    return session.get('authenticated', False)


def get_current_user():
    """Get current logged in user info"""
    return session.get('user', None)


def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    if user:
        return user["role"] == "admin"
    return False


def can_access_dashboard(dashboard_id):
    """Check if current user can access a specific dashboard"""
    user = get_current_user()
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


def get_accessible_dashboards():
    """Get list of dashboards accessible to current user"""
    user = get_current_user()
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
    users = get_users_db()
    
    if username not in users:
        return []
    
    user_data = users[username]
    if user_data["role"] == "admin" or user_data["dashboards"] == "all":
        return "all"
    
    return user_data.get("dashboards", [])


def get_readonly_users_for_dashboard(dashboard_id):
    """Get list of readonly users who have access to a specific dashboard"""
    users = get_users_db()
    
    readonly_users = []
    for username, user_data in users.items():
        if user_data["role"] == "readonly":
            if user_data["dashboards"] == "all" or dashboard_id in user_data.get("dashboards", []):
                readonly_users.append(user_data["name"])
    
    return readonly_users


# =============================================================================
# ADMIN FUNCTIONS
# =============================================================================

def get_all_users():
    """Get all users (admin only)"""
    return get_users_db()


def add_user(user_id, password, role, name, dashboards):
    """Add a new user (admin only)"""
    users = get_users_db()
    
    if user_id in users:
        return False, "User ID already exists"
    
    users[user_id] = {
        "password": password,
        "role": role,
        "name": name,
        "dashboards": dashboards if role == "readonly" else "all"
    }
    return True, "User created successfully"


def update_user(user_id, password=None, role=None, name=None, dashboards=None):
    """Update existing user (admin only)"""
    users = get_users_db()
    
    if user_id not in users:
        return False, "User not found"
    
    if password:
        users[user_id]["password"] = password
    if role:
        users[user_id]["role"] = role
        if role == "admin":
            users[user_id]["dashboards"] = "all"
    if name:
        users[user_id]["name"] = name
    if dashboards is not None and users[user_id]["role"] == "readonly":
        users[user_id]["dashboards"] = dashboards
    
    return True, "User updated successfully"


def delete_user(user_id):
    """Delete a user (admin only)"""
    users = get_users_db()
    
    if user_id not in users:
        return False, "User not found"
    
    if user_id == "admin":
        return False, "Cannot delete admin user"
    
    current_user = get_current_user()
    if current_user and current_user["username"] == user_id:
        return False, "Cannot delete yourself"
    
    del users[user_id]
    return True, "User deleted successfully"


def get_role_display(role):
    """Get display name for role"""
    return ROLE_DISPLAY.get(role, role)
