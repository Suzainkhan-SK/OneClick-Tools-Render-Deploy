import os
from supabase import create_client, Client

def create_supabase_client():
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and key must be set in environment variables")
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        raise

def handle_supabase_error(error):
    """Handle Supabase errors and return user-friendly messages"""
    error_message = str(error)
    
    # Common error messages to handle
    if "User already registered" in error_message:
        return "This email is already registered. Please try logging in instead."
    elif "Invalid login credentials" in error_message:
        return "Invalid email or password. Please try again."
    elif "Email not confirmed" in error_message:
        return "Please verify your email address before logging in."
    elif "Password should be at least" in error_message:
        return "Password is too weak. Please choose a stronger password."
    elif "Auth session missing" in error_message:
        return "Authentication required. Please log in again."
    else:
        return f"Authentication error: {error_message}"

def get_user_role(user_id):
    """Get user role from database"""
    try:
        supabase = create_supabase_client()
        response = supabase.table('user_profiles').select('preferences').eq('id', user_id).execute()
        
        if response.data:
            preferences = response.data[0].get('preferences', {})
            return preferences.get('role', 'user')
        return 'user'
    except Exception:
        return 'user'

def is_admin(user_id):
    """Check if user is admin"""
    return get_user_role(user_id) == 'admin'