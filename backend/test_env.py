import os
from dotenv import load_dotenv

load_dotenv()

print("Environment Variables Test")
print("=" * 30)
print(f"SECRET_KEY: {os.environ.get('SECRET_KEY')}")
print(f"SUPABASE_URL: {os.environ.get('SUPABASE_URL')}")
print(f"SUPABASE_KEY: {os.environ.get('SUPABASE_KEY')}")

if not os.environ.get('SUPABASE_URL') or not os.environ.get('SUPABASE_KEY'):
    print("\n❌ ERROR: Supabase environment variables are not set!")
    print("Please check your .env file in the backend directory")
else:
    print("\n✅ Environment variables are set correctly!")