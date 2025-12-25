import requests
import sys

def test_ollama_connection():
    """
    Test if the Ollama server is running and if the required models are available.
    """
    print("Testing Ollama server connection...")
    
    # Test server connection
    try:
        response = requests.get("http://localhost:11434/api/health")
        if response.status_code == 200:
            print("✅ Ollama server is running.")
        else:
            print(f"❌ Ollama server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server. Is it installed and running?")
        print("   To install Ollama, visit: https://ollama.com/")
        print("   After installation, run 'ollama serve' in a terminal.")
        return False
    
    # Test available models
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"Found {len(models)} models:")
            for model in models:
                print(f"  - {model.get('name')}")
            
            # Check for llama3.2-vision specifically
            llama_vision = any(model.get('name') == 'llama3.2-vision' for model in models)
            if llama_vision:
                print("✅ llama3.2-vision model is available.")
            else:
                print("❌ llama3.2-vision model is NOT available.")
                print("   To download it, run: ollama pull llama3.2-vision")
                return False
        else:
            print(f"❌ Failed to get model list: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking models: {e}")
        return False
    
    # Test a simple chat completion to verify API format
    try:
        print("\nTesting basic chat completion...")
        chat_data = {
            "model": "llama3.2-vision",
            "messages": [
                {"role": "user", "content": "Hello, are you working?"}
            ]
        }
        response = requests.post("http://localhost:11434/api/chat", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat completion API works! Sample response:")
            print(f"  {response.json().get('message', {}).get('content', '')[:50]}...")
        else:
            print(f"❌ Chat completion API returned error: {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing chat completion: {e}")
        return False
    
    print("\n✅ All tests passed! Ollama is correctly set up for your application.")
    return True

if __name__ == "__main__":
    success = test_ollama_connection()
    if not success:
        sys.exit(1)  # Exit with error code if tests failed
