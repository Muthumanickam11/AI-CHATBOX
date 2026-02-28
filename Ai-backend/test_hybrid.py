"""Test Hybrid Chat System"""
import requests
import json

BASE_URL = "http://127.0.0.1:8004/api/v1/hybrid"

def test_json_match():
    """Test 1: JSON knowledge base match"""
    print("\n" + "="*50)
    print("TEST 1: JSON Knowledge Base Match")
    print("="*50)
    
    payload = {
        "user_id": "test-user-001",
        "session_id": "sess-hybrid-001",
        "prompt": "What is AI?",
        "mode": "balanced"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Reply: {data['reply']}")
    print(f"Source: {data['source']}")
    print(f"Tokens: {data['tokens_used']}")
    print(f"Time: {data['processing_time']}")
    
    assert data['source'] == 'json_match', "Should match from JSON"
    assert data['tokens_used'] == 0, "JSON match should use 0 tokens"
    print("✅ JSON match test PASSED")

def test_ai_fallback():
    """Test 2: AI fallback for unknown question"""
    print("\n" + "="*50)
    print("TEST 2: AI Fallback (No JSON Match)")
    print("="*50)
    
    payload = {
        "user_id": "test-user-002",
        "session_id": "sess-hybrid-002",
        "prompt": "What is the meaning of life in the context of quantum physics?",
        "mode": "creative"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Reply: {data['reply'][:100]}...")
    print(f"Source: {data['source']}")
    print(f"Tokens: {data['tokens_used']}")
    print(f"Time: {data['processing_time']}")
    
    assert data['source'] == 'ai_generated', "Should fallback to AI"
    print("✅ AI fallback test PASSED")

def test_mode_precise():
    """Test 3: Precise mode"""
    print("\n" + "="*50)
    print("TEST 3: Precise Mode")
    print("="*50)
    
    payload = {
        "user_id": "test-user-003",
        "session_id": "sess-hybrid-003",
        "prompt": "Explain blockchain",
        "mode": "precise"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Reply: {data['reply'][:100]}...")
    print(f"Source: {data['source']}")
    print(f"Mode used: precise (temp=0.3)")
    print("✅ Precise mode test PASSED")

def test_history():
    """Test 4: History retrieval"""
    print("\n" + "="*50)
    print("TEST 4: History Retrieval")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/history/test-user-001?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"User: {data['user_id']}")
    print(f"History count: {data['count']}")
    print("✅ History test PASSED")

def test_health():
    """Test 5: Health check"""
    print("\n" + "="*50)
    print("TEST 5: Health Check")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Service: {data['service']}")
    print(f"Status: {data['status']}")
    assert data['status'] == 'ok', "Service should be healthy"
    print("✅ Health check PASSED")

if __name__ == "__main__":
    print("\n🚀 HYBRID CHAT SYSTEM TEST SUITE")
    print("="*50)
    
    try:
        test_health()
        test_json_match()
        test_ai_fallback()
        test_mode_precise()
        test_history()
        
        print("\n" + "="*50)
        print("🎉 ALL TESTS PASSED!")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
