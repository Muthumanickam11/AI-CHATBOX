import requests

def test_login():
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "email": "msdmuthu077@gmail.com",
        "password": "password123"
    }
    
    print(f"Attempting login to {url} with {payload['email']}...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
