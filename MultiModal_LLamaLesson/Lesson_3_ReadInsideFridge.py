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

## Know your fridge
disp_image("images/fridge-3.jpg")

question = ("What're in the fridge? What kind of food can be made? Give "
            "me 2 examples, based on only the ingredients in the fridge.")
base64_image = encode_image("images/fridge-3.jpg")
result = llama32pi(question, f"data:image/jpg;base64,{base64_image}")
print(result)


# ### Asking a follow up question
new_question = "is there banana in the fridge? where?"
messages = [
  {"role": "user", "content": [
      {"type": "text", "text": question},
      {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{base64_image}"}}
  ]},
  {"role": "assistant", "content": result},
  {"role": "user", "content": new_question}
]
result = llama32(messages)
print(result)


 
