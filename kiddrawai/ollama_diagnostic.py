import requests
import json
import base64
import sys

def diagnose_ollama_api():
    """Comprehensive diagnostic tool for Ollama API"""
    print("=== Ollama API Diagnostic Tool ===")
    
    # Check if the server is running
    try:
        health_response = requests.get("http://localhost:11434/api/health")
        print(f"Server health check: HTTP {health_response.status_code}")
        if health_response.status_code == 200:
            print("✅ Ollama server is running")
        else:
            print(f"❌ Ollama server returned unexpected status: {health_response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server at http://localhost:11434")
        print("Make sure Ollama is installed and running")
        return
    
    # Get available models
    try:
        models_response = requests.get("http://localhost:11434/api/tags")
        print("\n== Available Models ==")
        if models_response.status_code == 200:
            models_data = models_response.json()
            if "models" in models_data:
                for model in models_data["models"]:
                    print(f"- {model.get('name')}")
                
                # Check if mistral-small3.1:24b is available
                vision_model_available = any(
                    model.get("name") == "mistral-small3.1:24b" 
                    for model in models_data["models"]
                )
                if vision_model_available:
                    print("✅ mistral-small3.1:24b model is available")
                else:
                    print("❌ mistral-small3.1:24b model is NOT available")
                    print("Run 'ollama pull mistral-small3.1:24b' to download it")
            else:
                print(f"Unexpected response format: {models_data}")
        else:
            print(f"Failed to get models: HTTP {models_response.status_code}")
    except Exception as e:
        print(f"Error checking models: {e}")
    
    # Test different API endpoints
    print("\n== Testing API Endpoints ==")
    
    # 1. Test /api/chat with text-only
    print("\n1. Testing /api/chat with text-only message:")
    chat_payload = {
        "model": "mistral-small3.1:24b",
        "messages": [
            {"role": "user", "content": "Hello, what's your name?"}
        ],
        "stream": False
    }
    
    try:
        chat_response = requests.post("http://localhost:11434/api/chat", json=chat_payload)
        print(f"Status: HTTP {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            # First try to parse as regular JSON
            try:
                json_result = chat_response.json()
                print("Content type: Single JSON object")
                print(f"Response structure: {list(json_result.keys())}")
                if "message" in json_result:
                    print(f"Message role: {json_result['message'].get('role')}")
                    print(f"Content sample: {json_result['message'].get('content', '')[:100]}...")
                else:
                    print(f"Unexpected structure: {json_result}")
            except json.JSONDecodeError:
                # If that fails, it might be a streaming response
                print("Content type: Streaming JSON (multiple objects)")
                lines = chat_response.text.strip().split("\n")
                print(f"Number of JSON objects: {len(lines)}")
                if lines:
                    try:
                        first_obj = json.loads(lines[0])
                        print(f"First object keys: {list(first_obj.keys())}")
                    except:
                        print(f"Failed to parse first line: {lines[0][:100]}")
        else:
            print(f"Error response: {chat_response.text}")
    except Exception as e:
        print(f"Request error: {e}")
    
    # 2. Test /api/generate
    print("\n2. Testing /api/generate endpoint:")
    generate_payload = {
        "model": "mistral-small3.1:24b",
        "prompt": "Hello, what can you do?",
        "stream": False
    }
    
    try:
        generate_response = requests.post("http://localhost:11434/api/generate", json=generate_payload)
        print(f"Status: HTTP {generate_response.status_code}")
        
        if generate_response.status_code == 200:
            try:
                generate_result = generate_response.json()
                print(f"Response keys: {list(generate_result.keys())}")
                if "response" in generate_result:
                    print(f"Content sample: {generate_result['response'][:100]}...")
                else:
                    print(f"Unexpected structure: {generate_result}")
            except json.JSONDecodeError:
                print(f"Failed to parse as JSON: {generate_response.text[:100]}...")
        else:
            print(f"Error response: {generate_response.text}")
    except Exception as e:
        print(f"Request error: {e}")
    
    # Create a tiny 1x1 pixel image for testing
    print("\n3. Testing image handling with a tiny test image:")
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    
    # 3a. Test with /api/generate (typically more reliable for multimodal)
    print("\n3a. Testing image with /api/generate:")
    image_generate_payload = {
        "model": "mistral-small3.1:24b",
        "prompt": "What's in this image?",
        "images": [base64_image],
        "stream": False
    }
    
    try:
        image_response = requests.post("http://localhost:11434/api/generate", json=image_generate_payload)
        print(f"Status: HTTP {image_response.status_code}")
        
        if image_response.status_code == 200:
            try:
                image_result = image_response.json()
                print(f"Response keys: {list(image_result.keys())}")
                if "response" in image_result:
                    print(f"Content sample: {image_result['response'][:100]}...")
                else:
                    print(f"Unexpected structure: {image_result}")
            except json.JSONDecodeError:
                print(f"Failed to parse as JSON: {image_response.text[:100]}...")
        else:
            print(f"Error response: {image_response.text}")
    except Exception as e:
        print(f"Request error: {e}")
    
    # 3b. Test with /api/chat for images
    print("\n3b. Testing image with /api/chat:")
    image_chat_payload = {
        "model": "mistral-small3.1:24b",
        "messages": [
            {"role": "user", "content": "What's in this image?", "images": [base64_image]}
        ],
        "stream": False
    }
    
    try:
        image_chat_response = requests.post("http://localhost:11434/api/chat", json=image_chat_payload)
        print(f"Status: HTTP {image_chat_response.status_code}")
        
        if image_chat_response.status_code == 200:
            try:
                image_chat_result = image_chat_response.json()
                print(f"Response keys: {list(image_chat_result.keys())}")
                if "message" in image_chat_result:
                    print(f"Message role: {image_chat_result['message'].get('role')}")
                    print(f"Content sample: {image_chat_result['message'].get('content', '')[:100]}...")
                else:
                    print(f"Unexpected structure: {image_chat_result}")
            except json.JSONDecodeError:
                print(f"Failed to parse as JSON: {image_chat_response.text[:100]}...")
        else:
            print(f"Error response: {image_chat_response.text}")
    except Exception as e:
        print(f"Request error: {e}")
    
    print("\n=== Diagnostic Complete ===")
    print("Use these results to determine the correct API format for your application.")

if __name__ == "__main__":
    diagnose_ollama_api()
