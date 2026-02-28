import requests

def signup_muthu():
    url = "http://localhost:8000/api/v1/auth/signup"
    data = {
        "email": "muthu123@gmail.com",
        "password": "password123"
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Successfully signed up muthu123@gmail.com!")
        else:
            print(f"Failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    signup_muthu()
