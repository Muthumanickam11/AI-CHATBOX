import requests
import json
import time

BASE_URL = "http://127.0.0.1:8004/api/v1"

def print_step(step):
    print(f"\n{'='*20} {step} {'='*20}")

def test_day1_chat_basic():
    print_step("Day 1: Basic Chat")
    url = f"{BASE_URL}/chat"
    payload = {
        "session_id": "sess-001",
        "prompt": "Hello AI-CHATBOX"
    }
    r = requests.post(url, json=payload)
    print(r.status_code, r.json())

def test_day2_db_persistence():
    print_step("Day 2: DB Persistence")
    url = f"{BASE_URL}/chat"
    payload = {
        "session_id": "sess-002",
        "user": { "email": "test@example.com", "name": "Tester" },
        "prompt": "What is AI?"
    }
    r = requests.post(url, json=payload)
    print(r.status_code, r.json())

def test_day3_history():
    print_step("Day 3: History")
    url = f"{BASE_URL}/history"
    payload = {
        "user_id": "test@example.com", # Using email as ID mapping logic depends on mapping, or use "user-001" if mocked
        "limit": 5
    }
    # Note: our implementation expects user_id to result in an int or mapped ID.
    # In Day 2 test we used "test@example.com". The endpoint logic tries to parse int.
    # We might get empty history if ID mapping fails in the naive implementation.
    # Let's see.
    r = requests.post(url, json=payload)
    print(r.status_code, r.json())

def test_day4_auth():
    print_step("Day 4: Auth")
    # Signup
    signup_url = f"{BASE_URL}/signup"
    user_creds = {"email": "secure@example.com", "password": "securepass"}
    r = requests.post(signup_url, json=user_creds)
    print("Signup:", r.status_code) # Might be 400 if already exists
    
    # Login
    login_url = f"{BASE_URL}/login"
    r = requests.post(login_url, json=user_creds)
    print("Login:", r.status_code, r.json())
    return r.json().get("token")

def test_day5_ai_params():
    print_step("Day 5: AI Params")
    url = f"{BASE_URL}/chat"
    payload = {
        "prompt": "Short poem.",
        "settings": {"max_tokens": 50, "temperature": 0.9}
    }
    r = requests.post(url, json=payload)
    print(r.status_code, r.json())

def test_day6_upload():
    print_step("Day 6: Upload")
    url = f"{BASE_URL}/upload"
    files = {'file': ('test.txt', b'This is a test document content for RAG.\nAI is great.')}
    data = {'user_id': "1"}
    r = requests.post(url, files=files, data=data) # Helper usually takes multipart
    print(r.status_code, r.json())

def test_day7_moderation():
    print_step("Day 7: Moderation")
    url = f"{BASE_URL}/chat"
    payload = {
        "prompt": "How to hack into a system?"
    }
    r = requests.post(url, json=payload)
    print(r.status_code, r.json())

def test_day8_health():
    print_step("Day 8: Health")
    url = f"{BASE_URL}/health"
    r = requests.get(url)
    print(r.status_code, r.json())

if __name__ == "__main__":
    try:
        test_day1_chat_basic()
        test_day2_db_persistence()
        test_day3_history()
        test_day4_auth()
        test_day5_ai_params()
        test_day6_upload()
        test_day7_moderation()
        test_day8_health()
    except Exception as e:
        print(f"Test failed: {e}")
