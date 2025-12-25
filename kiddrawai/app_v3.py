import gradio as gr
import warnings
import base64
import random
import os
import requests
#from google.cloud import translate_v2 as translate
from utils import load_env, llama32, disp_image
warnings.filterwarnings('ignore')
load_env()

def kid_draw_analysis(image_path, initial_question, followup_question):
    """Analyze children's artwork with kid-friendly responses"""
    if image_path is None:
        return "Please upload your amazing artwork! 🎨"
    
    if not initial_question.strip():
        initial_question = (
            "You are a friendly art teacher. Look at this child's drawing"
            "1. Give an enthusiastic and encouraging description of what you see "
            "2. Point out specific creative elements you notice "
            "3. Ask the child an interesting question about their artwork. "
            "4. The first response keep not more than 50 words "
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

def get_random_example():
    """Get a random example image from the list"""
    examples = ["Example_1.jpeg", "Example_2.jpeg", "Example_3.jpeg", 
                "Example_4.jpeg", "Example_5.jpeg", "Example_6.jpeg", 
                "Example_7.jpeg", "Example_8.jpeg", "Example_9.jpeg"]
    selected = random.choice(examples)
    # Check if file exists and return path
    if os.path.exists(selected):
        return selected
    return None

def translate_text_libre(text, target_language):
    """Translate text using LibreTranslate API (doesn't require API key for basic usage)"""
    if target_language == "English":
        return text
    
    try:
        # Map the display language to the language code
        language_code = ""
        if "Traditional Chinese" in target_language:
            language_code = "zh-TW"
        elif "Simplified Chinese" in target_language:
            language_code = "zh-CN"
        
        # Use LibreTranslate API
        API_URL = "https://libretranslate.com/translate"
        response = requests.post(API_URL, 
            data={
                "q": text,
                "source": "en",
                "target": language_code,
            }
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()["translatedText"]
        else:
            return f"{text}\n\n[Translation Error: {response.status_code}]"
    
    except Exception as e:
        return f"{text}\n\n[Translation Error: {str(e)}]"

# Function to handle form submission and clear inputs
def submit_and_clear(image_path, initial_question, followup_question):
    # Get analysis result
    result = kid_draw_analysis(image_path, initial_question, followup_question)
    
    # Return result and clear input fields
    # Note: We keep the image but clear text inputs
    return result, "", ""

# Create Gradio interface with compact layout
with gr.Blocks(
    title="KnowKidDraw - Your Digital Art Gallery!",
    css="""
    #app-container {
        max-width: 480px !important;  /* Smartphone width or 1/4 of a 24-inch monitor */
        margin: 0 auto !important;
    }
    .contain {
        max-width: 480px !important;
        margin: 0 auto !important;
    }
    """
) as demo:
    with gr.Group(elem_id="app-container"):
        gr.Markdown("# 🎨 KnowKidDraw")
        
        # Initialize with a random example
        image_input = gr.Image(
            type="filepath",
            label="Upload Your Drawing Here! 🎨",
            value=get_random_example(),  # Set initial random example
            height=300,  # Control image height
            width=400    # Control image width
        )
        
        initial_q = gr.Textbox(
            label="☺️ Tell me about your drawing?",
            placeholder="Leave blank and I'll tell you what I see!",
            lines=2
        )
        
        followup_q = gr.Textbox(
            label="Ask me about your drawing:",
            placeholder="Any questions about my analysis?",
            lines=2
        )
        
        draw_button = gr.Button("✨ Show Me The Magic! ✨", size="lg")
        
        art_output = gr.Textbox(
            label="Your Art Story", 
            lines=6
        )
        
        # Language selection in a more compact layout
        with gr.Row():
            language_dropdown = gr.Dropdown(
                choices=[
                    "English", 
                    "Traditional Chinese (繁體中文), enable later", 
                    "Simplified Chinese (简体中文), enable later"
                ],
                label="Language",
                value="English"
            )
            translate_button = gr.Button("🌐 Translate")
        
        # Add a clear button that resets everything and loads a new random example
        clear_button = gr.Button("🔄 Start Over with a New Drawing")
        
        # Instructions in a collapsible section to save space
        with gr.Accordion("Instructions", open=False):
            gr.Markdown("""
            ## Welcome Young Artists! 🌈
            1. Upload your drawing or use our example
            2. Tell us about your drawing (or leave it blank)
            3. Click the magic button
            4. Ask follow-up questions if you want
            5. Try different languages with the translate button
            """)
            
    # Function to reset the interface with a new random example
    def reset_interface():
        return get_random_example(), "", "", ""
        
    # Use updated function that clears inputs after submission
    draw_button.click(
        fn=submit_and_clear,
        inputs=[image_input, initial_q, followup_q],
        outputs=[art_output, initial_q, followup_q]
    )
    
    # Add click handler for the clear button
    clear_button.click(
        fn=reset_interface,
        inputs=[],
        outputs=[image_input, initial_q, followup_q, art_output]
    )
    
    # Add click handler for translation
    translate_button.click(
        fn=translate_text_libre,
        inputs=[art_output, language_dropdown],
        outputs=[art_output]
    )

if __name__ == "__main__":
    # Set a smaller default height and width for the interface
    demo.launch(height=800, width=500)
