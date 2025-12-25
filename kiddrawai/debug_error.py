import requests
import base64
import sys

def test_llama32_api():
    """Test if the Ollama API works with a simple text message and image."""
    print("Testing Ollama API for llama32-vision model...")
    
    # Basic text-only message test
    print("\n1. Testing basic text message:")
    payload = {
        "model": "llama3.2-vision:90b",
        
        "messages": [
            {"role": "user", "content": "Hello, are you working?"}
        ]
    }
    
    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        if response.status_code == 200:
            print("✅ Basic text message works!")
            print(f"Response: {response.json().get('message', {}).get('content', '')[:50]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Let's create a very simple test image (a colored rectangle)
    print("\n2. Testing with a simple base64 image:")
    # This is a 1x1 pixel red dot in base64
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    
    # Try with the format your code appears to be using (including images array)
    payload = {
        "model": "llama3.2-vision:90b",
        "messages": [
            {
                "role": "user",
                "content": "What's in this image?",
                "images": [base64_image]
            }
        ]
    }
    
    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        if response.status_code == 200:
            print("✅ Image message works!")
            print(f"Response: {response.json().get('message', {}).get('content', '')[:50]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Now test the exact format from your application code (for comparison)
    print("\n3. Testing with the format from your application code:")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    
    # Print the structure for debugging
    print(f"Message structure: {messages}")
    
    # Extract the base64 data from the messages
    base64_data = None
    for msg in messages:
        content = msg['content']
        if isinstance(content, list):
            for item in content:
                if item['type'] == 'image_url':
                    image_url = item['image_url']['url']
                    if image_url.startswith('data:image'):
                        base64_data = image_url.split(',')[1]
    
    # Create the payload as in your application
    payload = {
        "model": "llama3.2-vision:90b",
        "messages": [
            {
                "role": "user",
                "content": "What's in this image?",
                "images": [base64_data]
            }
        ]
    }
    
    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        if response.status_code == 200:
            print("✅ Application format works!")
            print(f"Response: {response.json().get('message', {}).get('content', '')[:50]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print("\nTesting complete. Use the results to fix your llama32 function.")

if __name__ == "__main__":
    test_llama32_api()
