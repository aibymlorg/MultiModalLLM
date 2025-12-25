import gradio as gr
import warnings
import base64
from utils import load_env, llama32, disp_image, merge_images, resize_image
warnings.filterwarnings('ignore')
load_env()

def encode_image(image_file):
    return base64.b64encode(image_file).decode('utf-8')

def llama32pi(prompt, image_url, model_size=90):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]
    return llama32(messages, model_size)

def llama32repi(question, image_url, result, new_question, model_size=90):
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]},
        {"role": "assistant", "content": result},
        {"role": "user", "content": new_question}
    ]
    return llama32(messages, model_size)

def interior_design(image):
    if image is None:
        return "Please upload an image."
    
    with open(image, "rb") as image_file:
        image_b64 = encode_image(image_file.read())
    question = ("Describe the design, style, color, material and other "
                "aspects of the fireplace in this photo. Then list all "
                "the objects in the photo.")
    
    result = llama32pi(question, f"data:image/jpeg;base64,{image_b64}")
    
    new_question = ("How many balls and vases are there? Which one is closer "
                    "to the fireplace: the balls or the vases?")
    final_result = llama32repi(question, f"data:image/jpeg;base64,{image_b64}", 
                              result, new_question)
    
    return f"{result}\n\nAdditional Analysis:\n{final_result}"

def read_receipts(images):
    if not images:
        return "Please upload receipt images."
    
    results = []
    total_response = ""
    
    for image in images:
        image_b64 = encode_image(image)
        result = llama32pi("What's the total charge in the receipt?", 
                          f"data:image/jpeg;base64,{image_b64}")
        results.append(result)
        total_response += f"{result}\n"
    
    # Calculate total from all receipts
    messages = [{"role": "user", 
                "content": f"What's the total charge of all the receipts below?\n{total_response}"}]
    total = llama32(messages)
    
    return f"Individual Receipts:\n{total_response}\nTotal Analysis:\n{total}"

def graph_to_table(image):
    if image is None:
        return "Please upload a graph image."
    
    image_b64 = encode_image(image)
    result = llama32pi("Convert the chart to an HTML table.", 
                      f"data:image/png;base64,{image_b64}")
    
    return result

# Create Gradio interface
with gr.Blocks(title="Multimodal LLama Analysis") as demo:
    gr.Markdown("# Multimodal LLama Analysis")
    
    with gr.Tab("Interior Design"):
        with gr.Row():
            image_input = gr.Image(type="filepath", label="Upload Interior Image")
            design_output = gr.Textbox(label="Analysis Result")
        design_button = gr.Button("Analyze Interior")
        design_button.click(fn=interior_design, 
                          inputs=image_input, 
                          outputs=design_output)
    
    with gr.Tab("Read Receipts"):
        with gr.Row():
            receipts_input = gr.File(file_count="multiple", label="Upload Receipts")
            receipts_output = gr.Textbox(label="Receipt Analysis")
        receipts_button = gr.Button("Analyze Receipts")
        receipts_button.click(fn=read_receipts, 
                            inputs=receipts_input, 
                            outputs=receipts_output)
    
    with gr.Tab("Graph to Table"):
        with gr.Row():
            graph_input = gr.Image(type="filepath", label="Upload Graph")
            table_output = gr.HTML(label="Table Output")
        graph_button = gr.Button("Convert to Table")
        graph_button.click(fn=graph_to_table, 
                         inputs=graph_input, 
                         outputs=table_output)

if __name__ == "__main__":
    demo.launch()
