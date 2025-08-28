import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def test_supabase_connection():
    try:
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection by selecting from a table
        print("Testing Supabase connection...")
        
        # Try to select from users table
        try:
            result = supabase.table('users').select('count', count='exact').execute()
            print(f"✅ Users table accessible. Count: {result.count}")
        except Exception as e:
            print(f"⚠️  Users table error: {e}")
            print("This might be normal if the table doesn't exist yet")
        
        # Test auth connection
        try:
            auth_test = supabase.auth.get_session()
            print("✅ Auth service accessible")
        except Exception as e:
            print(f"⚠️  Auth service error: {e}")
        
        print("✅ Supabase connection test completed!")
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")

if __name__ == '__main__':
    test_supabase_connection()