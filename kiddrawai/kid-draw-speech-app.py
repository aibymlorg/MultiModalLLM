import gradio as gr
import warnings
import base64
from utils import load_env, llama32, disp_image
warnings.filterwarnings('ignore')
load_env()

def kid_draw_analysis(image_path, audio_initial, audio_followup):
    """Analyze children's artwork with kid-friendly responses and handle audio input"""
    if image_path is None:
        return "Please upload your amazing artwork! 🎨", None
    
    # Convert audio questions to text or use default prompt
    initial_question = audio_initial if audio_initial else (
        "You are a friendly art teacher. Look at this child's drawing and: "
        "1. Give an enthusiastic and encouraging description of what you see "
        "2. Point out specific creative elements you notice "
        "3. Ask the child an interesting question about their artwork. "
        "Keep your response fun and engaging for children."
    )
    
    # First analysis
    result = process_image_for_llama(image_path, initial_question)
    
    # Follow-up analysis if provided
    if audio_followup:
        base64_image = encode_image_for_llama(image_path)
        messages = [
            {"role": "user", 
             "content": [
                 {"type": "text", "text": initial_question},
                 {"type": "image_url", 
                  "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
             ]},
            {"role": "assistant", "content": result},
            {"role": "user", "content": audio_followup}
        ]
        final_result = llama32(messages)
        complete_response = f"{result}\n\nMore about your artwork:\n{final_result}"
    else:
        complete_response = result
    
    return complete_response, complete_response  # Return both text and audio content

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
with gr.Blocks(title="KidDraw - Your Talking Art Gallery!") as demo:
    gr.Markdown("# 🎨 KidDraw - Let's Talk About Your Art! 🖼️")
    
    with gr.Tab("KidDraw Gallery"):
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    type="filepath",
                    label="Upload Your Drawing Here! 🎨"
                )
                
                gr.Markdown("### 🎤 Tell me about your drawing!")
                initial_audio = gr.Audio(
                    source="microphone",
                    type="text",
                    label="Record your first question",
                    placeholder="Click to record your question!",
                )
                
                followup_audio = gr.Audio(
                    source="microphone",
                    type="text",
                    label="Ask another question!",
                    placeholder="Click to ask another question!",
                )
                
                draw_button = gr.Button("✨ Magic Art Talk Button! ✨")
            
            with gr.Column(scale=1):
                # Text output for reading
                text_output = gr.Textbox(
                    label="Your Art Story (Text)", 
                    lines=10,
                    visible=True
                )
                
                # Audio output for listening
                audio_output = gr.Audio(
                    label="Listen to Your Art Story! 🔊",
                    type="text",
                    visible=True
                )
        
        draw_button.click(
            fn=kid_draw_analysis,
            inputs=[
                image_input,
                initial_audio,
                followup_audio
            ],
            outputs=[
                text_output,
                audio_output
            ]
        )
        
        gr.Markdown("""
        ## Let's Talk About Your Art! 🌈
        1. Upload your drawing
        2. Click the microphone and tell me about your drawing
        3. Press the magic button
        4. Listen to what I see in your art!
        5. Ask another question if you want to know more!
        
        Remember: You can always read the text too! 📖
        """)

if __name__ == "__main__":
    demo.launch()
