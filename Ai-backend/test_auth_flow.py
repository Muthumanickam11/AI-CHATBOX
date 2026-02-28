import requests

def test_auth():
    base_url = "http://localhost:8000/api/v1/auth"
    
    # Try login first - should fail with 401
    print("Testing login with new user...")
    resp = requests.post(f"{base_url}/login", json={"email": "muthu_test@gmail.com", "password": "password123"})
    print(f"Login Response: {resp.status_code} - {resp.text}")
    
    # Try signup - should succeed with 200
    print("\nTesting signup with new user...")
    resp = requests.post(f"{base_url}/signup", json={"email": "muthu_test@gmail.com", "password": "password123"})
    print(f"Signup Response: {resp.status_code} - {resp.text}")
    
    # Try login again - should succeed with 200
    print("\nTesting login again after signup...")
    resp = requests.post(f"{base_url}/login", json={"email": "muthu_test@gmail.com", "password": "password123"})
    print(f"Login Response: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    test_auth()
