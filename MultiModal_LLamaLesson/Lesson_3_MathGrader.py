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


## Math grader

disp_image("images/math_hw3.jpg")

prompt = ("Check carefully each answer in a kid's math homework, first "
          "do the calculation, then compare the result with the kid's "
          "answer, mark correct or incorrect for each answer, and finally"
          " return a total score based on all the problems answered.")
base64_image = encode_image("images/math_hw3.jpg")
result = llama32pi(prompt, f"data:image/jpg;base64,{base64_image}")
print(result)

