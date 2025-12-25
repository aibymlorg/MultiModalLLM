# Add this to your existing utils.py
import requests
import json

from dotenv import load_dotenv, find_dotenv
import os
from wolframalpha import Client

def load_env():
    _ = load_dotenv(find_dotenv())

  # The right API to pass in a prompt (of type string) is the completions API https://docs.together.ai/reference/completions-1
  # The right API to pass in a messages (of type of list of message) is The chat completions API https://docs.together.ai/reference/chat-completions-1

import ollama
def llama32(messages, model_size=None):  # model_size parameter kept for compatibility
    """
    Send requests to local Ollama llama3.2-vision model
    """
    url = "http://localhost:11434/v1"
    #llm_teach = ChatOpenAI(model = "Llama3.1", base_url = "http://localhost:11434/v1")
    # Convert Together AI format to Ollama format
    ollama_messages = []
    for msg in messages:
        content = msg['content']
        if isinstance(content, list):
            # Handle multimodal content
            ollama_content = []
            for item in content:
                if item['type'] == 'text':
                    ollama_content.append({
                        'type': 'text',
                        'text': item['text']
                    })
                elif item['type'] == 'image_url':
                    # Handle base64 images
                    image_url = item['image_url']['url']
                    if image_url.startswith('data:image'):
                        base64_data = image_url.split(',')[1]
                        ollama_content.append({
                            'type': 'image',
                            'data': base64_data
                        })
            content = ollama_content
        
        ollama_messages.append({
            'role': msg['role'],
            'content': content
        })


#response = ollama.chat(
#        model='llama3.2-vision',
#        messages=[{
#            'role': 'user',
#            'content': 'What is in this image?',
#            'images': ['image.jpg']
#        }]
#    )
#
#    print(response)


    payload = {
        "model": "llama3.2-vision",
        "messages": ollama_messages,
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['message']['content']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama local host Error: {str(e)}")

import os
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def disp_image(address):
    if address.startswith("http://") or address.startswith("https://"):
        response = requests.get(address)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(address)
    
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def resize_image(img, max_dimension = 1120):
  original_width, original_height = img.size

  if original_width > original_height:
      scaling_factor = max_dimension / original_width
  else:
      scaling_factor = max_dimension / original_height

  new_width = int(original_width * scaling_factor)
  new_height = int(original_height * scaling_factor)

  # Resize the image while maintaining aspect ratio
  resized_img = img.resize((new_width, new_height))

  resized_img.save("images/resized_image.jpg")

  print("Original size:", original_width, "x", original_height)
  print("New size:", new_width, "x", new_height)

  return resized_img


from PIL import Image

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
    
    merged_image.save("images/merged_image_horizontal.jpg")
    
    print("Merged image dimensions:", merged_image.size)
    return merged_image



# pretty print JSON with syntax highlighting
from pygments import highlight, lexers, formatters
def cprint(response):
    formatted_json = json.dumps(response, indent=4)
    colorful_json = highlight(formatted_json,
                              lexers.JsonLexer(),
                              formatters.TerminalFormatter())
    print(colorful_json)

import nest_asyncio
nest_asyncio.apply()

def wolfram_alpha(query: str) -> str:
    WOLFRAM_ALPHA_KEY = get_wolfram_alpha_api_key()
    client = Client(WOLFRAM_ALPHA_KEY)
    result = client.query(query)

    results = []
    for pod in result.pods:
        if pod["@title"] == "Result" or pod["@title"] == "Results":
          for sub in pod.subpods:
            results.append(sub.plaintext)

    return '\n'.join(results)



def get_boiling_point(liquid_name, celsius):
  # function body
  return []
