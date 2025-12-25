# # Multimodal Use Case

import warnings
warnings.filterwarnings('ignore')

from utils import load_env
load_env()
utils import llama32
import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def llama32pi(prompt, image_url, model_size=90):
  messages = [
    {
      "role": "user",
      "content": [
        {"type": "text",
          "text": prompt},
        {"type": "image_url",
          "image_url": {
            "url": image_url}
        }
      ]
    },
  ]

  result = llama32(messages, model_size)
  return result


## Choosing the right drink
disp_image("images/drinks.png")

question = "I am on a diet. Which drink should I drink?"

base64_image = encode_image("images/drinks.png")
result = llama32pi(question, f"data:image/png;base64,{base64_image}")
print(result)

question = ("Generete nurtrition facts of the two drinks " 
            "in JSON format for easy comparison.")
result = llama32pi(question, f"data:image/png;base64,{base64_image}")
print(result)
