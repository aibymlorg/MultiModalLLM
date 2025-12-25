import gradio as gr
import warnings
import base64
from utils import load_env, llama32, disp_image, merge_images, resize_image
from PIL import Image
import io
warnings.filterwarnings('ignore')
load_env()

def encode_image_for_llama(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_for_llama(image_path, prompt):
    """Process image and create message structure for llama32"""
    base64_image = encode_image_for_llama(image_path)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", 
                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    return llama32(messages)

def interior_design(image_path):
    """Analyze interior design image"""
    if image_path is None:
        return "Please upload an image."
    
    # First analysis
    initial_prompt = ("Describe the design, style, color, material and other "
                     "aspects of the fireplace in this photo. Then list all "
                     "the objects in the photo.")
    result = process_image_for_llama(image_path, initial_prompt)
    
    # Follow-up analysis
    followup_prompt = ("How many balls and vases are there? Which one is closer "
                      "to the fireplace: the balls or the vases?")
    
    # Create messages for follow-up
    base64_image = encode_image_for_llama(image_path)
    messages = [
        {"role": "user", 
         "content": [
             {"type": "text", "text": initial_prompt},
             {"type": "image_url", 
              "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
         ]},
        {"role": "assistant", "content": result},
        {"role": "user", "content": followup_prompt}
    ]
    
    final_result = llama32(messages)
    return f"{result}\n\nAdditional Analysis:\n{final_result}"

def read_receipts(files):
    """Analyze multiple receipt images"""
    if not files:
        return "Please upload receipt images."
    
    results = []
    total_response = ""
    
    # Process each receipt
    for file in files:
        temp_path = file.name  # Gradio creates temporary files
        result = process_image_for_llama(temp_path, 
                                       "What's the total charge in the receipt?")
        results.append(result)
        total_response += f"{result}\n"
    
    # Calculate total from all receipts
    messages = [
        {"role": "user", 
         "content": f"What's the total charge of all the receipts below?\n{total_response}"}
    ]
    total = llama32(messages)
    
    return f"Individual Receipts:\n{total_response}\nTotal Analysis:\n{total}"

def graph_to_table(image_path):
    """Convert graph to HTML table"""
    if image_path is None:
        return "Please upload a graph image."
    
    result = process_image_for_llama(image_path, 
                                   "Convert the chart to an HTML table.")
    return result

# Create Gradio interface
with gr.Blocks(title="Multimodal LLama Analysis") as demo:
    gr.Markdown("# Multimodal LLama Analysis")
    
    with gr.Tab("Interior Design"):
        with gr.Row():
            image_input = gr.Image(type="filepath", label="Upload Interior Image")
            design_output = gr.Textbox(label="Analysis Result", lines=10)
        design_button = gr.Button("Analyze Interior")
        design_button.click(fn=interior_design, 
                          inputs=image_input, 
                          outputs=design_output)
    
    with gr.Tab("Read Receipts"):
        with gr.Row():
            receipts_input = gr.File(file_count="multiple", label="Upload Receipts")
            receipts_output = gr.Textbox(label="Receipt Analysis", lines=10)
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
