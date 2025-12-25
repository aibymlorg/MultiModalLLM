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

def llama32repi(question, image_url, result, new_question, model_size=90):
    messages = [
      {"role": "user", "content": [
          {"type": "text", "text": question},
          {"type": "image_url", "image_url": {"url": image_url}}
      ]},
      {"role": "assistant", "content": result},
      {"role": "user", "content": new_question}
    ]
    result = llama32(messages, model_size)
    return result


## Interior Design Assistant
disp_image("images/001.jpeg")

question = ("Describe the design, style, color, material and other "
            "aspects of the fireplace in this photo. Then list all "
            "the objects in the photo.")
base64_image = encode_image("images/001.jpeg")
result = llama32pi(question, f"data:image/jpeg;base64,{base64_image}")
print(result)

new_question = ("How many balls and vases are there? Which one is closer "
                "to the fireplace: the balls or the vases?")
res = llama32repi(question, f"data:image/jpeg;base64,{base64_image}", result, new_question)
print(res)

disp_image("images/001.jpeg")

 
