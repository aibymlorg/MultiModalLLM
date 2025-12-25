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

## OCR with receipts

from utils import disp_image
for i in range(1, 4):
  disp_image(f"images/receipt-{i}.jpg")

question = "What's the total charge in the receipt?"
results = ""
for i in range(1, 4):
    base64_image = encode_image(f"images/receipt-{i}.jpg")
    res = llama32pi(question, f"data:image/jpeg;base64,{base64_image}")
    results = results + f"{res}\n"
print(results)

messages = [
    {"role": "user",
     "content": f"""What's the total charge of all the recipts below?
{results}"""
  }
]

response = llama32(messages)
print(response)

## Handling multiple images
from utils import merge_images
import matplotlib.pyplot as plt
merged_image = merge_images("images/receipt-1.jpg",
                            "images/receipt-2.jpg",
                            "images/receipt-3.jpg")
plt.imshow(merged_image)
plt.axis('off')
plt.show()

from utils import resize_image
resized_img = resize_image(merged_image)

base64_image = encode_image("images/resized_image.jpg")
question = "What's the total charge of all the recipts below?"
result = llama32pi(question,
                      f"data:image/jpeg;base64,{base64_image}")
print(result)
 
