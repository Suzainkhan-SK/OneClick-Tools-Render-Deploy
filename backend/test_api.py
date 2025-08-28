import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:5000"
    
    print("Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test registration endpoint
    try:
        data = {
            "email": "cmpunktg@gmail.com",
            "password": "@Suzainkhan6361",
            "fullName": "CM Punk"
        }
        response = requests.post(f"{base_url}/api/register", 
                               json=data,
                               headers={"Content-Type": "application/json"})
        print(f"Registration: {response.status_code} - {response.text}")
        
        # If registration successful, test login
        if response.status_code == 201:
            login_data = {
                "email": "cmpunktg@gmail.com",
                "password": "@Suzainkhan6361"
            }
            login_response = requests.post(f"{base_url}/api/login", 
                                         json=login_data,
                                         headers={"Content-Type": "application/json"})
            print(f"Login: {login_response.status_code} - {login_response.text}")
            
            # If login successful, test getting user data
            if login_response.status_code == 200:
                # Save the session cookie for authenticated requests
                session_cookie = login_response.cookies.get('session')
                headers = {
                    "Content-Type": "application/json",
                    "Cookie": f"session={session_cookie}"
                }
                
                user_response = requests.get(f"{base_url}/api/user", headers=headers)
                print(f"User data: {user_response.status_code} - {user_response.text}")
                
    except Exception as e:
        print(f"API test failed: {e}")

if __name__ == "__main__":
    test_api_endpoints()