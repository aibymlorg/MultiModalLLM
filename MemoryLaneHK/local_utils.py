import requests
import json
from dotenv import load_dotenv, find_dotenv
import os
from wolframalpha import Client
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from pygments import highlight, lexers, formatters

def load_env():
    _ = load_dotenv(find_dotenv())

def llama32(messages, model_size=11):
    """
    Send messages to local Ollama API for Llama 3.2 Vision model
    Uses the correct Ollama API format as per documentation
    """
    url = "http://localhost:11434/api/chat"
    
    # Extract text content and images separately
    final_messages = []
    
    for msg in messages:
        content = msg['content']
        message_text = ""
        images = []
        
        if isinstance(content, list):
            # Handle multimodal content - extract text and images
            text_parts = []
            for item in content:
                if item['type'] == 'text':
                    text_parts.append(item['text'])
                elif item['type'] == 'image_url':
                    # Extract base64 image data
                    image_url = item['image_url']['url']
                    if image_url.startswith('data:image'):
                        base64_data = image_url.split(',')[1]
                        images.append(base64_data)
            
            message_text = ' '.join(text_parts)
        else:
            message_text = content
        
        # Create message in Ollama format
        ollama_message = {
            'role': msg['role'],
            'content': message_text
        }
        
        # Add images if present (only for user messages in Ollama)
        if images and msg['role'] == 'user':
            ollama_message['images'] = images
            
        final_messages.append(ollama_message)
    
    # Prepare payload for Ollama API
    payload = {
        "model": "llama3.2-vision",
        "messages": final_messages,
        "stream": False
    }
    
    try:
        print(f"Sending request to: {url}")
        print(f"Payload (without image data): {json.dumps({**payload, 'messages': [{**msg, 'images': '[IMAGES_PRESENT]' if 'images' in msg else None} for msg in payload['messages']]}, indent=2)}")
        
        response = requests.post(url, json=payload, timeout=300)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 404:
            return "Error: Ollama server not found. Please ensure Ollama is running and llama3.2-vision model is installed. Run: 'ollama pull llama3.2-vision'"
        
        response.raise_for_status()
        result = response.json()
        
        print(f"Response structure: {list(result.keys())}")
        
        # Extract content from Ollama response
        if 'message' in result and 'content' in result['message']:
            return result['message']['content']
        else:
            return f"Unexpected response format: {result}"
            
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama server. Please ensure Ollama is running on localhost:11434"
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model might be processing a large image."
    except requests.exceptions.RequestException as e:
        return f"Error making request to Ollama: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error parsing response: {str(e)} - Response text: {response.text[:500]}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def test_ollama_connection():
    """Test if Ollama is running and llama3.2-vision is available"""
    try:
        # Test basic connection
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json()
            model_names = [model['name'] for model in models.get('models', [])]
            
            if any('llama3.2-vision' in name for name in model_names):
                return "✓ Ollama is running and llama3.2-vision is available"
            else:
                return f"✗ Ollama is running but llama3.2-vision not found. Available models: {model_names}"
        else:
            return f"✗ Ollama responded with status {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "✗ Cannot connect to Ollama. Please start Ollama server with 'ollama serve'"
    except Exception as e:
        return f"✗ Error checking Ollama: {str(e)}"

def get_wolfram_alpha_api_key():
    load_env()
    wolfram_alpha_api_key = os.getenv("WOLFRAM_ALPHA_KEY")
    return wolfram_alpha_api_key

def get_tavily_api_key():
    load_env()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    return tavily_api_key

def llama31(prompt_or_messages, model_size=8, temperature=0, raw=False, debug=False):
    """
    Function for Llama 3.1 (text-only) via Together AI
    """
    model = f"meta-llama/Meta-Llama-3.1-{model_size}B-Instruct-Turbo"
    if isinstance(prompt_or_messages, str):
        prompt = prompt_or_messages
        url = f"{os.getenv('DLAI_TOGETHER_API_BASE', 'https://api.together.xyz')}/v1/completions"
        payload = {
            "model": model,
            "temperature": temperature,
            "prompt": prompt
        }
    else:
        messages = prompt_or_messages
        url = f"{os.getenv('DLAI_TOGETHER_API_BASE', 'https://api.together.xyz')}/v1/chat/completions"
        payload = {
            "model": model,
            "temperature": temperature,
            "messages": messages
        }

    if debug:
        print(payload)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"
    }

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(payload)
        )
        response.raise_for_status()
        res = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")

    if 'error' in res:
        raise Exception(f"API Error: {res['error']}")

    if raw:
        return res

    if isinstance(prompt_or_messages, str):
        return res['choices'][0].get('text', '')
    else:
        return res['choices'][0].get('message', {}).get('content', '')

def disp_image(address):
    if address.startswith("http://") or address.startswith("https://"):
        response = requests.get(address)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(address)
    
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def resize_image(img, max_dimension=1120):
    original_width, original_height = img.size

    if original_width > original_height:
        scaling_factor = max_dimension / original_width
    else:
        scaling_factor = max_dimension / original_height

    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)

    # Resize the image while maintaining aspect ratio
    resized_img = img.resize((new_width, new_height))

    # Ensure images directory exists
    os.makedirs("images", exist_ok=True)
    resized_img.save("images/resized_image.jpg")

    print("Original size:", original_width, "x", original_height)
    print("New size:", new_width, "x", new_height)

    return resized_img

def merge_images(image_1, image_2, image_3):
    img1 = Image.open(image_1)
    img2 = Image.open(image_2)
    img3 = Image.open(image_3)
    
    width1, height1 = img1.size
    width2, height2 = img2.size
    width3, height3 = img3.size
    
    print("Image 1 dimensions:", width1, height1)
    print("Image 2 dimensions:", width2, height2)
    print("Image 3 dimensions:", width3, height3)
    
    total_width = width1 + width2 + width3
    max_height = max(height1, height2, height3)
    
    merged_image = Image.new("RGB", (total_width, max_height))
    
    merged_image.paste(img1, (0, 0))
    merged_image.paste(img2, (width1, 0))
    merged_image.paste(img3, (width1 + width2, 0))
    
    # Ensure images directory exists
    os.makedirs("images", exist_ok=True)
    merged_image.save("images/merged_image_horizontal.jpg")
    
    print("Merged image dimensions:", merged_image.size)
    return merged_image

def cprint(response):
    """Pretty print JSON with syntax highlighting"""
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json,
                              lexers.JsonLexer(),
                              formatters.TerminalFormatter())
    print(colorful_json)

def wolfram_alpha(query: str) -> str:
    WOLFRAM_ALPHA_KEY = get_wolfram_alpha_api_key()
    if not WOLFRAM_ALPHA_KEY:
        return "Wolfram Alpha API key not found"
    
    try:
        client = Client(WOLFRAM_ALPHA_KEY)
        result = client.query(query)

        results = []
        for pod in result.pods:
            if pod["@title"] == "Result" or pod["@title"] == "Results":
                for sub in pod.subpods:
                    if sub.plaintext:
                        results.append(sub.plaintext)

        return '\n'.join(results) if results else "No results found"
    except Exception as e:
        return f"Error querying Wolfram Alpha: {str(e)}"

def get_boiling_point(liquid_name, celsius):
    # Placeholder function - implement as needed
    return []