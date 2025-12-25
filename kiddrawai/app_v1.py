import gradio as gr
import warnings
import base64
from utils import load_env, llama32, disp_image
warnings.filterwarnings('ignore')
load_env()

def kid_draw_analysis(image_path, initial_question, followup_question):
    """Analyze children's artwork with kid-friendly responses"""
    if image_path is None:
        return "Please upload your amazing artwork! 🎨"
    
    if not initial_question.strip():
        initial_question = (
            "You are a friendly art teacher. Look at this child's drawing and using tradional chinese: "
            "1. Give an enthusiastic and encouraging description of what you see "
            "2. Point out specific creative elements you notice "
            "3. Ask the child an interesting question about their artwork. "
            "4. The first response keep not more than 50 words"
            "Keep your response fun and engaging for children."
        )
    
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
        return f"{result}\n\nMore about your artwork:\n{final_result}"
    
    return result

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

# Create Gradio interface
with gr.Blocks(title="KidDraw - Your Digital Art Gallery!") as demo:
    gr.Markdown("# 🎨 KidDraw - Share Your Amazing Artwork! 🖼️")
    
    with gr.Tab("KidDraw Gallery"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(
                    type="filepath",
                    label="Upload Your Drawing Here! 🎨"
                )
                initial_q = gr.Textbox(
                    label="What would you like to tell me about your drawing? ✏️",
                    placeholder="Leave blank if you prefer not to tell me and let me tell you what I see!",
                    visible=True
                )
                followup_q = gr.Textbox(
                    label="Ask me any questions what I said about your drawings 😉",
                    placeholder="Let me learn from you if I am wrong about your drawing?",
                    visible=True
                )
                draw_button = gr.Button("✨ Show Me The Magic! ✨")
            
            art_output = gr.Textbox(
                label="Your Art Story", 
                lines=10
            )
            
        draw_button.click(
            fn=kid_draw_analysis,
            inputs=[image_input, initial_q, followup_q],
            outputs=art_output
        )
        
        gr.Markdown("""
        ## Welcome Young Artists! 🌈
        1. Upload your drawing
        2. Ask a question about it (or leave it blank and I'll tell you what I see!)
        3. Click the magic button
        4. Ask another question if you want to know more!
        """)

if __name__ == "__main__":
    demo.launch()
