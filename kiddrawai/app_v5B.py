import gradio as gr
import warnings
import base64
import random
import os
import requests
from utils import load_env, llama32, disp_image, ollama_vision, get_available_ollama_models, check_ollama_connection
warnings.filterwarnings('ignore')
load_env()

def kid_draw_analysis(image_path, initial_question, model_choice):
    """Analyze children's artwork with kid-friendly responses"""
    if image_path is None:
        return "Please upload your amazing artwork! 🎨"
    
    if not initial_question.strip():
        initial_question = (
            "You are a friendly art teacher. Look at this child's drawing. "
            "1. Give an enthusiastic and encouraging description of what you see "
            "2. Point out specific creative elements you notice "
            "3. Ask the child an interesting question about their artwork. "
            "4. The first response keep not more than 50 words "
            "Keep your response fun and engaging for children."
        )
    
    # Choose the appropriate model function
    if model_choice.startswith("Ollama"):
        model_name = model_choice.split(" - ")[1] if " - " in model_choice else "llava:34b"
        result = process_image_for_ollama(image_path, initial_question, model_name)
    else:
        # Default to llama32 (Together AI)
        result = process_image_for_llama(image_path, initial_question)
    
    return result

def follow_up_analysis(image_path, initial_response, followup_question, model_choice):
    """Process follow-up questions about the artwork"""
    if not followup_question.strip():
        return initial_response
    
    if image_path is None:
        return initial_response
    
    # Choose the appropriate model function
    if model_choice.startswith("Ollama"):
        model_name = model_choice.split(" - ")[1] if " - " in model_choice else "llava:34b"
        
        base64_image = encode_image_for_ollama(image_path)
        messages = [
            {"role": "user", 
             "content": "Look at this child's drawing and give feedback",
             "images": [base64_image]},
            {"role": "assistant", "content": initial_response},
            {"role": "user", "content": followup_question}
        ]
        final_result = ollama_vision(messages, model_name)
    else:
        # Default to llama32 (Together AI)
        base64_image = encode_image_for_llama(image_path)
        messages = [
            {"role": "user", 
             "content": [
                 {"type": "text", "text": "Look at this child's drawing and give feedback"},
                 {"type": "image_url", 
                  "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
             ]},
            {"role": "assistant", "content": initial_response},
            {"role": "user", "content": followup_question}
        ]
        final_result = llama32(messages)
    
    return f"{initial_response}\n\nMore about your artwork:\n{final_result}"

def encode_image_for_llama(image_path):
    """Convert image to base64 string for Together AI models"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def encode_image_for_ollama(image_path):
    """Convert image to base64 string for Ollama models"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_for_llama(image_path, prompt):
    """Process image and create message structure for llama32 (Together AI)"""
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

def process_image_for_ollama(image_path, prompt, model="llava:34b"):
    """Process image and create message structure for Ollama models"""
    base64_image = encode_image_for_ollama(image_path)
    messages = [
        {
            "role": "user",
            "content": prompt,
            "images": [base64_image]
        }
    ]
    return ollama_vision(messages, model)

def get_model_choices():
    """Get available model choices including Ollama models"""
    choices = ["Together AI - Llama 3.2 Vision (Default)"]
    
    # Check if Ollama is available and get models
    if check_ollama_connection():
        available_models = get_available_ollama_models()
        target_models = ["llava:34b", "llama4:scout", "qwen2.5v1:72b"]
        
        for model in target_models:
            # Check for exact match or partial match (in case of different tags)
            matching_models = [m for m in available_models if model in m or m.startswith(model.split(':')[0])]
            if matching_models:
                # Use the first matching model
                choices.append(f"Ollama - {matching_models[0]}")
        
        # Add any other vision models that might be available
        vision_keywords = ["llava", "vision", "multimodal", "qwen", "llama4"]
        for model in available_models:
            model_lower = model.lower()
            if any(keyword in model_lower for keyword in vision_keywords):
                ollama_choice = f"Ollama - {model}"
                if ollama_choice not in choices:
                    choices.append(ollama_choice)
    else:
        choices.append("Ollama - Not Available (Start Ollama service)")
    
    return choices

def get_example_gif():
    """Use the Example.gif as the initial example"""
    if os.path.exists("Example.gif"):
        return "Example.gif"
    else:
        # Fallback to a random JPEG if the GIF doesn't exist
        return get_random_example()

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

# Placeholder functions for speech features
def speech_to_text_placeholder():
    return "Enable speech to text later"

def text_to_speech_placeholder():
    return "Enable text to speech later"

def refresh_models():
    """Refresh the available models list"""
    return gr.update(choices=get_model_choices(), value=get_model_choices()[0])

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
    /* Make the image container take full width of the app container */
    .image-container img {
        width: 100% !important;
        max-width: 100% !important;
    }
    /* Style for the icon buttons - SMALLER SIZE */
    .icon-button {
        font-size: 16px !important;  /* Reduced from 24px */
        cursor: pointer;
        padding: 2px 6px !important;  /* Reduced padding */
        border-radius: 50%;
        background: #f0f0f0;
        border: none;
        min-width: 24px !important;  /* Force smaller width */
        min-height: 24px !important; /* Force smaller height */
        line-height: 1 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .icon-button:hover {
        background: #ffebf3;
        color: #ff69b4;
    }
    /* Add some spacing between sections */
    .conversation-section {
        margin-top: 15px;
        border-top: 1px solid #eee;
        padding-top: 15px;
    }
    /* Model selection styling */
    .model-section {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    """
) as demo:
    with gr.Group(elem_id="app-container"):
        gr.Markdown("# 🎨 KnowKidDraw")
        
        # Instructions in a collapsible section moved to the top
        with gr.Accordion("Instructions", open=False):
            gr.Markdown("""
            ## Welcome Young Artists! 🌈
            1. Choose your preferred AI model (Together AI or local Ollama models)
            2. Upload your drawing or use our example
            3. Tell us about your drawing (or leave it blank)
            4. Click the magic button 🧙 to see the AI's response
            5. Ask more questions about your artwork to continue the conversation
            6. Try different languages with the translate button (enable in MVP)
            7. Option to use microphone 🎤 and speaker 🔈 in the device (enable in MVP)
            8. Option to use professional advices (enable in MVP)
            
            ### Available Models:
            - **Together AI**: Cloud-based Llama 3.2 Vision (requires API key)
            - **Ollama Local**: Your local models (llava:34b, llama4:scout, qwen2.5v1:72b)
            """)
        
        # Model selection section
        with gr.Group(elem_classes="model-section"):
            gr.Markdown("### 🤖 Choose Your AI Art Critic")
            with gr.Row():
                model_dropdown = gr.Dropdown(
                    choices=get_model_choices(),
                    label="AI Model",
                    value=get_model_choices()[0],
                    scale=4
                )
                refresh_button = gr.Button("🔄", elem_classes="icon-button", scale=1, 
                                         elem_id="refresh-models")
        
        # Initialize with the GIF example - now full width
        image_input = gr.Image(
            type="filepath",
            label="Upload Your Drawing Here! 🎨",
            value=get_example_gif(),  # Set initial random example
            height=300,
            width="100%"    # Control image width
        )
        
        # Speech status for feedback
        speech_status = gr.Textbox(
            label="Status",
            visible=False
        )
        
        # Initial question section
        with gr.Row():
            initial_q = gr.Textbox(
                label="☺️ Tell me about your drawing?",
                placeholder="Leave blank and I'll tell you what I see!",
                lines=2,
                scale=10
            )
            mic_button = gr.Button("🎤", elem_classes="icon-button", scale=1)
        
        # Initial analysis button
        draw_button = gr.Button("✨ Show Me The Magic! ✨", size="lg")
        
        # Output with speech output icon
        with gr.Row():
            art_output = gr.Textbox(
                label="Your Art Story", 
                lines=6,
                scale=10
            )
            speaker_button = gr.Button("🔊", elem_classes="icon-button", scale=1)
        
        # Follow-up conversation section - moved after the output
        with gr.Group(elem_classes="conversation-section"):
            with gr.Row():
                followup_q = gr.Textbox(
                    label="Am I understanding your drawing?",
                    placeholder="Ask me more about what I said...",
                    lines=2,
                    scale=10
                )
                mic_button2 = gr.Button("🎤", elem_classes="icon-button", scale=1)
            
            followup_button = gr.Button("💬 Tell Me More", size="md")
        
        # Language selection in a more compact layout
        with gr.Row():
            language_dropdown = gr.Dropdown(
                choices=[
                    "English", 
                    "Traditional Chinese (繁體中文), enable later", 
                    "Simplified Chinese (简體中文), enable later"
                ],
                label="Language",
                value="English"
            )
            translate_button = gr.Button("🌐 Translate")
        
        # Add a clear button that resets everything and loads a new drawing example
        clear_button = gr.Button("🔄 Start Over with a New Drawing")
    
    # Add click handlers for the microphone buttons - simplified
    mic_button.click(
        fn=speech_to_text_placeholder,
        inputs=[],
        outputs=[speech_status]
    )
    
    mic_button2.click(
        fn=speech_to_text_placeholder,
        inputs=[],
        outputs=[speech_status]
    )
    
    # Add click handler for the speaker button - simplified
    speaker_button.click(
        fn=text_to_speech_placeholder,
        inputs=[],
        outputs=[speech_status]
    )
    
    # Add click handler for the refresh models button
    refresh_button.click(
        fn=refresh_models,
        inputs=[],
        outputs=[model_dropdown]
    )
            
    # Function to reset the interface with a new random example
    def reset_interface():
        # Start with GIF again for first reset, then use random JPEGs
        if os.path.exists("Example.gif"):
            return "Example.gif", "", "", gr.update(visible=False)
        else:
            return get_random_example(), "", "", gr.update(visible=False)
    
    # Initial analysis
    draw_button.click(
        fn=kid_draw_analysis,
        inputs=[image_input, initial_q, model_dropdown],
        outputs=[art_output]
    )
    
    # Follow-up analysis
    followup_button.click(
        fn=follow_up_analysis,
        inputs=[image_input, art_output, followup_q, model_dropdown],
        outputs=[art_output]
    ).then(
        fn=lambda: "",  # Clear the followup question field after submission
        inputs=[],
        outputs=[followup_q]
    )
    
    # Add click handler for the clear button
    clear_button.click(
        fn=reset_interface,
        inputs=[],
        outputs=[image_input, initial_q, art_output, speech_status]
    ).then(
        fn=lambda: "",  # Also clear followup field
        inputs=[],
        outputs=[followup_q]
    )
    
    # Add click handler for translation
    translate_button.click(
        fn=translate_text_libre,
        inputs=[art_output, language_dropdown],
        outputs=[art_output]
    )

if __name__ == "__main__":
    # Set a smaller default height and width for the interface
    demo.launch(height=700, width=500)