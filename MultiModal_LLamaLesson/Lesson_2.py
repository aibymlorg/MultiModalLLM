#!/usr/bin/env python
# coding: utf-8

#Llama 3.2 Multimodal Prompting

import warnings
warnings.filterwarnings('ignore')

from utils import load_env
load_env()

## Text input only question

from utils import llama32
from utils import llama31

messages = [
  {"role": "user",
    "content": "Who wrote the book Charlotte's Web?"}
]

response_32 = llama32(messages, 90)
print(response_32)

response_31 = llama31(messages,70)
print(response_31)

messages = [
  {"role": "user",
    "content": "Who wrote the book Charlotte's Web?"},
      {"role": "assistant",
    "content": response_32},
      {"role": "user",
    "content": "3 of the best quotes"}
]


response_32 = llama32(messages,90)
print(response_32)

response_31 = llama31(messages,70)
print(response_31)

## Question about an image

from utils import disp_image

disp_image("images/Llama_Repo.jpeg") # Example usage for local image

## Image from a URL

image_url = ("https://raw.githubusercontent.com/meta-llama/"
            "llama-models/refs/heads/main/Llama_Repo.jpeg")
messages = [
  {"role": "user",
    "content": [
      {"type": "text",
        "text": "describe the image in one sentence"
      },
      {"type": "image_url",
        "image_url": {"url": image_url}
      }
    ]
  },
]

disp_image(image_url)
result = llama32(messages,90)
print(result)


## Using a local image

import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
base64_image = encode_image("images/Llama_Repo.jpeg")

messages = [
  {"role": "user",
    "content": [
      {"type": "text",
        "text": "describe the image in one sentence"
      },
      {"type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
      }
    ]
  },
]

disp_image(image_url)
result = llama32(messages,90)
print(result)


## Follow up question about an image
messages = [
  {"role": "user",
    "content": [
      {"type": "text",
        "text": "describe the image in one sentence"
      },
      {"type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
      }
    ]
  },
  {"role": "assistant", "content": result},
  {"role": "user", "content": "how many of them are purple?"}
]

result = llama32(messages)
print(result)


## Define llama32pi() helper
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

print(llama32pi("describe the image in one sentence",
                "https://raw.githubusercontent.com/meta-llama/"
                "llama-models/refs/heads/main/Llama_Repo.jpeg"))

print(llama32pi("describe the image in one sentence",
                f"data:image/jpeg;base64,{base64_image}"))

##Plant recognition

disp_image("images/tree.jpg")

question = ("What kind of plant is this in my garden?"
            "Describe it in a short paragraph.")

base64_image = encode_image("images/tree.jpg")
result = llama32pi(question, f"data:image/jpg;base64,{base64_image}")
print(result)


## Dog breed recognition

disp_image("images/ww1.jpg")

question = (("What dog breed is this? Describe in one paragraph,"
             "and 3-5 short bullet points"))
base64_image = encode_image("images/ww1.jpg")
result = llama32pi(question, f"data:image/jpg;base64,{base64_image}")
print(result)

disp_image("images/ww2.png")

base64_image = encode_image("images/ww2.png")
result = llama32pi(question, f"data:image/png;base64,{base64_image}")
print(result)


## Tire pressure warning

disp_image("images/tire_pressure.png")

question = (("What's the problem this is about?"
             " What should be good numbers?"))

base64_image = encode_image("images/tire_pressure.png")
result = llama32pi(question, f"data:image/png;base64,{base64_image}")
print(result)

