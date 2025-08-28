#!/usr/bin/env python3
"""
Test script to verify all required packages are installed correctly
"""

try:
    import flask
    print("✓ Flask installed successfully")
except ImportError:
    print("✗ Flask not installed")

try:
    import flask_cors
    print("✓ Flask-CORS installed successfully")
except ImportError:
    print("✗ Flask-CORS not installed")

try:
    import dotenv
    print("✓ python-dotenv installed successfully")
except ImportError:
    print("✗ python-dotenv not installed")

try:
    import supabase
    print("✓ supabase installed successfully")
except ImportError:
    print("✗ supabase not installed")

try:
    import dateutil
    print("✓ python-dateutil installed successfully")
except ImportError:
    print("✗ python-dateutil not installed")

# Test basic functionality
try:
    from supabase import create_client
    print("✓ Supabase client can be imported")
except Exception as e:
    print(f"✗ Supabase client import failed: {e}")

print("\nTest completed!")