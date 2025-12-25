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


# ## Tool calling with image

disp_image("images/golden_gate.png")


question = ("Where is the location of the place shown in the picture?")
base64_image = encode_image("images/golden_gate.png")
result = llama32pi(question, f"data:image/png;base64,{base64_image}")
print(result)

weather_question = ("What is the current weather in the location "
                 "mentioned in the text below: \n"  f"{result}")
print(weather_question)

from datetime import datetime

current_date = datetime.now()
formatted_date = current_date.strftime("%d %B %Y")

messages = [
    {"role": "system",
     "content":  f"""
Environment: ipython
Tools: brave_search, wolfram_alpha
Cutting Knowledge Date: December 2023
Today Date: {formatted_date}
"""},
    {"role": "user",
     "content": weather_question}
  ]
print(llama32(messages))
