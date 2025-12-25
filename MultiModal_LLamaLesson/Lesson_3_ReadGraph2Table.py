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


## Llama 3.1 70B Instruct model speed
disp_image("images/llama31speed.png")

question = "Convert the chart to an HTML table."
base64_image = encode_image("images/llama31speed.png")
result = llama32pi(question, f"data:image/png;base64,{base64_image}")
print(result)

from IPython.display import HTML
minified_html_table = "<table><thead><tr><th>Model</th><th>Output Tokens per Second</th></tr></thead><tbody><tr><td>Llama 2 1.5B</td><td>217</td></tr><tr><td>Google's PaLM 2 540B</td><td>214</td></tr><tr><td>Google's PaLM 2 540B</td><td>163</td></tr><tr><td>Meta's LLaMA 2 70B</td><td>133</td></tr><tr><td>Meta's LLaMA 2 70B</td><td>129</td></tr><tr><td>Google's T5 3.5B</td><td>123</td></tr><tr><td>OPT-6B</td><td>111</td></tr><tr><td>OPT-6B</td><td>75</td></tr><tr><td>ChatGPT-3.5</td><td>64</td></tr><tr><td>Google's T5 3.5B</td><td>62</td></tr><tr><td>Google's T5 3.5B</td><td>61</td></tr><tr><td>Meta's LLaMA 2 7B</td><td>68</td></tr><tr><td>Meta's LLaMA 2 7B</td><td>38</td></tr><tr><td>Meta's LLaMA 2 7B</td><td>38</td></tr><tr><td>Meta's LLaMA 2 7B</td><td>25</td></tr></tbody></table>"
HTML(minified_html_table)
