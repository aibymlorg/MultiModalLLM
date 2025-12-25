import gradio as gr
import warnings
import base64
from ollama_utils import load_env, llama32, disp_image, merge_images, resize_image
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

def interior_design(image_path, initial_question, followup_question):
    """Analyze interior design image with custom questions"""
    if image_path is None:
        return "Please upload an image."
    
    if not initial_question.strip():
        initial_question = ("Describe the design, style, color, material and other "
                          "aspects of the fireplace in this photo. Then list all "
                          "the objects in the photo.")
    
    # First analysis
    result = process_image_for_llama(image_path, initial_question)
    
    # Follow-up analysis if provided
    if followup_question.strip():
        base64_image = encode_image_for_llama(image_path)
        messages = [
            {"role": "user", 
             "content": [
                 {"type": "text", "text": initial_question},
                 {"type": "image_url", 
                  "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
             ]},
            {"role": "assistant", "content": result},
            {"role": "user", "content": followup_question}
        ]
        final_result = llama32(messages)
        return f"{result}\n\nFollow-up Analysis:\n{final_result}"
    
    return result

def read_receipts(files, question, summary_question):
    """Analyze multiple receipt images with custom questions"""
    if not files:
        return "Please upload receipt images."
    
    if not question.strip():
        question = "What's the total charge in the receipt?"
        
    if not summary_question.strip():
        summary_question = "What's the total charge of all the receipts below?"
    
    results = []
    total_response = ""
    
    # Process each receipt
    for file in files:
        temp_path = file.name
        result = process_image_for_llama(temp_path, question)
        results.append(result)
        total_response += f"{result}\n"
    
    # Calculate total using custom summary question
    messages = [
        {"role": "user", 
         "content": f"{summary_question}\n{total_response}"}
    ]
    total = llama32(messages)
    
    return f"Individual Receipts:\n{total_response}\nSummary Analysis:\n{total}"

def graph_to_table(image_path, question):
    """Convert graph to HTML table with custom question"""
    if image_path is None:
        return "Please upload a graph image."
    
    if not question.strip():
        question = "Convert the chart to an HTML table."
    
    result = process_image_for_llama(image_path, question)
    return result

# Create Gradio interface
with gr.Blocks(title="Multimodal LLama Analysis") as demo:
    gr.Markdown("# Multimodal LLama Analysis")
    
    with gr.Tab("Interior Design"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(type="filepath", label="Upload Interior Image")
                initial_q = gr.Textbox(
                    label="Initial Question", 
                    placeholder="Describe the design, style, color, material...")
                followup_q = gr.Textbox(
                    label="Follow-up Question (Optional)",
                    placeholder="Ask a follow-up question based on the initial analysis")
                design_button = gr.Button("Analyze Interior")
            design_output = gr.Textbox(label="Analysis Result", lines=10)
        design_button.click(
            fn=interior_design, 
            inputs=[image_input, initial_q, followup_q], 
            outputs=design_output)
    
    with gr.Tab("Read Receipts"):
        with gr.Row():
            with gr.Column():
                receipts_input = gr.File(file_count="multiple", label="Upload Receipts")
                receipt_q = gr.Textbox(
                    label="Question for Each Receipt",
                    placeholder="What's the total charge in the receipt?")
                summary_q = gr.Textbox(
                    label="Summary Question",
                    placeholder="What's the total charge of all the receipts?")
                receipts_button = gr.Button("Analyze Receipts")
            receipts_output = gr.Textbox(label="Receipt Analysis", lines=10)
        receipts_button.click(
            fn=read_receipts, 
            inputs=[receipts_input, receipt_q, summary_q], 
            outputs=receipts_output)
    
    with gr.Tab("Graph to Table"):
        with gr.Row():
            with gr.Column():
                graph_input = gr.Image(type="filepath", label="Upload Graph")
                graph_q = gr.Textbox(
                    label="Question",
                    placeholder="Convert the chart to an HTML table")
                graph_button = gr.Button("Convert to Table")
            table_output = gr.HTML(label="Table Output")
        graph_button.click(
            fn=graph_to_table, 
            inputs=[graph_input, graph_q], 
            outputs=table_output)

if __name__ == "__main__":
    demo.launch()
