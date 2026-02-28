import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_step(day, test_name):
    print(f"\n{'='*60}")
    print(f"  {day}: {test_name}")
    print(f"{'='*60}")

def test_day1_basic_chat():
    """Day 1: Backend Foundation & Environment Setup"""
    print_step("DAY 1", "Basic Chat Connection")
    
    url = f"{BASE_URL}/chat"
    payload = {
        "session_id": "sess-001",
        "prompt": "Hello AI-CHATBOX, what can you do?"
    }
    
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
    assert r.status_code == 200
    assert "reply" in r.json() or "answer" in r.json()
    print("✓ Day 1 Test Passed")

def test_day2_db_persistence():
    """Day 2: Database Integration & User Context"""
    print_step("DAY 2", "Database Integration & User Context")
    
    url = f"{BASE_URL}/chat"
    payload = {
        "user": { "email": "lush@example.com", "name": "Lush" },
        "prompt": "Explain Artificial Intelligence in simple words."
    }
    
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    response = r.json()
    print(f"Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert "conversation_id" in response
    assert response.get("stored") == True
    print("✓ Day 2 Test Passed")

def test_day3_history():
    """Day 3: Chat History & Retrieval"""
    print_step("DAY 3", "Chat History & Retrieval")
    
    # First create some chat history
    chat_url = f"{BASE_URL}/chat"
    for i, prompt in enumerate(["Hello", "What is AI?", "Tell me more"]):
        payload = {
            "user": { "email": "history_user@example.com", "name": "History User" },
            "prompt": prompt
        }
        requests.post(chat_url, json=payload)
    
    # Now retrieve history
    history_url = f"{BASE_URL}/history"
    payload = {
        "user_id": "1",  # Assuming first user
        "action": "get_history",
        "limit": 3
    }
    
    r = requests.post(history_url, json=payload)
    print(f"Status: {r.status_code}")
    response = r.json()
    print(f"Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert "history" in response
    assert "count" in response
    print("✓ Day 3 Test Passed")

def test_day4_auth():
    """Day 4: Authentication Layer"""
    print_step("DAY 4", "Authentication Layer")
    
    # Signup
    signup_url = f"{BASE_URL}/signup"
    user_creds = {"email": "lush@example.com", "password": "securepass"}
    r = requests.post(signup_url, json=user_creds)
    print(f"Signup Status: {r.status_code}")
    
    # Login
    login_url = f"{BASE_URL}/login"
    r = requests.post(login_url, json=user_creds)
    print(f"Login Status: {r.status_code}")
    response = r.json()
    print(f"Login Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert "token" in response
    assert response.get("login_status") == "success"
    assert "expires_in" in response
    print("✓ Day 4 Test Passed")
    return response.get("token")

def test_day5_ai_params():
    """Day 5: AI Logic & Model Configuration"""
    print_step("DAY 5", "AI Logic & Model Configuration")
    
    url = f"{BASE_URL}/chat"
    payload = {
        "user_id": "user-001",
        "conversation_id": "conv-101",
        "query": "List benefits of renewable energy.",
        "settings": { "temperature": 0.7, "max_tokens": 200 }
    }
    
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    response = r.json()
    print(f"Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert "answer" in response or "reply" in response
    assert "tokens_used" in response
    assert "processing_time" in response
    print("✓ Day 5 Test Passed")

def test_day6_upload():
    """Day 6: Document Ingestion / RAG Pipeline"""
    print_step("DAY 6", "Document Ingestion / RAG Pipeline")
    
    url = f"{BASE_URL}/upload"
    files = {'file': ('ai_intro.txt', b'Artificial Intelligence systems learn from data to make decisions. AI is transforming industries.')}
    data = {'user_id': "user-001"}
    
    r = requests.post(url, files=files, data=data)
    print(f"Upload Status: {r.status_code}")
    response = r.json()
    print(f"Upload Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert "doc_id" in response
    assert "embedding_status" in response
    assert "chunks_indexed" in response
    print("✓ Day 6 Test Passed")

def test_day7_moderation():
    """Day 7: Moderation + Analytics"""
    print_step("DAY 7", "Moderation + Analytics")
    
    url = f"{BASE_URL}/chat"
    payload = {
        "user_id": "user-001",
        "prompt": "How to hack a system?"
    }
    
    r = requests.post(url, json=payload)
    print(f"Status: {r.status_code}")
    response = r.json()
    print(f"Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert response.get("status") == "blocked"
    assert response.get("reason") == "unsafe_content"
    print("✓ Day 7 Test Passed")

def test_day8_health():
    """Day 8: Deployment + Monitoring"""
    print_step("DAY 8", "Deployment + Monitoring")
    
    url = f"{BASE_URL}/health"
    r = requests.get(url)
    print(f"Status: {r.status_code}")
    response = r.json()
    print(f"Health Response: {json.dumps(response, indent=2)}")
    assert r.status_code == 200
    assert response.get("status") == "healthy"
    assert "uptime" in response
    assert "requests_today" in response
    assert "average_latency" in response
    assert "error_rate" in response
    print("✓ Day 8 Test Passed")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  AI-CHATBOX BACKEND - 8-DAY COMPLETE TEST SUITE")
    print("="*60)
    
    try:
        test_day1_basic_chat()
        test_day2_db_persistence()
        test_day3_history()
        test_day4_auth()
        test_day5_ai_params()
        test_day6_upload()
        test_day7_moderation()
        test_day8_health()
        
        print("\n" + "="*60)
        print("  ✓ ALL TESTS PASSED!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
