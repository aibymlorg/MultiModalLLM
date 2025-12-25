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
    print(f"DEBUG: image_path = {image_path}")
    print(f"DEBUG: model_choice = {model_choice}")
    
    if image_path is None:
        return "Please upload your amazing artwork! 🎨"
    
    # Check if file exists
    if not os.path.exists(image_path):
        return f"Sorry, I can't find the image file. Please try uploading again! 🎨"
    
    if not initial_question.strip():
        initial_question = (
            "You are a friendly art teacher. Look at this child's drawing. "
            "1. Give an enthusiastic and encouraging description of what you see "
            "2. Point out specific creative elements you notice "
            "3. Honesty is important, if you do anything, just be nice to say it"
            "4. Ask the child an interesting question about their artwork. "
            "5. The first response keep not more than 70 words "
            "Keep your response fun and engaging for children."
        )
    
    try:
        # Choose the appropriate model function
        if model_choice.startswith("Ollama"):
            model_name = model_choice.split(" - ")[1] if " - " in model_choice else "llava:34b"
            result = process_image_for_ollama(image_path, initial_question, model_name)
        else:
            # Default to llama32 (Together AI)
            result = process_image_for_llama(image_path, initial_question)
        
        return result
        
    except Exception as e:
        print(f"DEBUG: Error in kid_draw_analysis: {e}")
        return f"Oops! Something went wrong while analyzing your artwork. Error: {str(e)} 🎨 Please try again!"

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
    try:
        print(f"DEBUG: Encoding image for Llama: {image_path}")
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            print(f"DEBUG: Successfully encoded image, length: {len(encoded)}")
            return encoded
    except Exception as e:
        print(f"DEBUG: Error encoding image for Llama: {e}")
        raise

def encode_image_for_ollama(image_path):
    """Convert image to base64 string for Ollama models"""
    try:
        print(f"DEBUG: Encoding image for Ollama: {image_path}")
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            print(f"DEBUG: Successfully encoded image, length: {len(encoded)}")
            return encoded
    except Exception as e:
        print(f"DEBUG: Error encoding image for Ollama: {e}")
        raise

def process_image_for_llama(image_path, prompt):
    """Process image and create message structure for llama32 (Together AI)"""
    try:
        print(f"DEBUG: Processing image for Llama: {image_path}")
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
        print("DEBUG: Calling llama32...")
        result = llama32(messages)
        print(f"DEBUG: Llama32 result: {result[:100]}...")
        return result
    except Exception as e:
        print(f"DEBUG: Error in process_image_for_llama: {e}")
        raise

def process_image_for_ollama(image_path, prompt, model="llava:34b"):
    """Process image and create message structure for Ollama models"""
    try:
        print(f"DEBUG: Processing image for Ollama: {image_path}, model: {model}")
        base64_image = encode_image_for_ollama(image_path)
        messages = [
            {
                "role": "user",
                "content": prompt,
                "images": [base64_image]
            }
        ]
        print("DEBUG: Calling ollama_vision...")
        result = ollama_vision(messages, model)
        print(f"DEBUG: Ollama result: {result[:100]}...")
        return result
    except Exception as e:
        print(f"DEBUG: Error in process_image_for_ollama: {e}")
        raise

def get_model_choices():
    """Get available model choices including Ollama models"""
    choices = ["Together AI - Llama 3.2 Vision"]
    
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
        choices.append("Ollama - Service Not Running")
    
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
    return "Speech to text feature coming soon..."

def text_to_speech_placeholder():
    return "Text to speech feature coming soon..."

def refresh_models():
    """Refresh the available models list"""
    return gr.update(choices=get_model_choices(), value=get_model_choices()[0])

# Create Gradio interface with responsive mobile-first design
with gr.Blocks(
    title="🎨 KnowKidDraw - AI Art Gallery",
    css="""
    /* Mobile-first responsive design */
    .gradio-container {
        max-width: 100% !important;
        margin: 0 auto !important;
        padding: 10px !important;
    }
    
    /* Container size based on screen */
    @media (min-width: 768px) {
        .gradio-container {
            max-width: 600px !important;
            padding: 20px !important;
        }
    }
    
    @media (min-width: 1200px) {
        .gradio-container {
            max-width: 800px !important;
            padding: 30px !important;
        }
    }
    
    /* Main title - responsive sizing */
    .main-title {
        text-align: center;
        font-size: 1.8em !important;
        font-weight: bold !important;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
        margin-bottom: 15px !important;
    }
    
    @media (min-width: 768px) {
        .main-title {
            font-size: 2.2em !important;
            margin-bottom: 20px !important;
        }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Image section - mobile optimized */
    .image-section {
        margin-bottom: 15px;
    }
    
    .image-section .image-container {
        min-height: 250px !important;
        border-radius: 15px;
        overflow: hidden;
        border: 3px solid #f0f0f0;
    }
    
    @media (min-width: 768px) {
        .image-section .image-container {
            min-height: 350px !important;
        }
    }
    
    @media (min-width: 1200px) {
        .image-section .image-container {
            min-height: 450px !important;
        }
    }
    
    /* Model selection - more compact */
    .model-selection {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 12px;
        color: white;
    }
    
    .model-selection label {
        color: white !important;
        font-weight: bold;
        font-size: 13px !important;
    }
    
    @media (min-width: 768px) {
        .model-selection {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 15px;
        }
        .model-selection label {
            font-size: 14px !important;
        }
    }
    
    /* Input sections */
    .input-section {
        margin-bottom: 12px;
    }
    
    .input-section textarea,
    .input-section input {
        font-size: 15px !important; /* Prevents zoom on mobile */
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px !important;
        font-family: system-ui, -apple-system, sans-serif !important;
    }
    
    @media (min-width: 768px) {
        .input-section textarea,
        .input-section input {
            font-size: 16px !important;
            padding: 14px !important;
        }
    }
    
    /* Response area - larger and more prominent */
    .response-section {
        margin: 15px 0;
    }
    
    .response-section textarea {
        min-height: 180px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 16px !important;
        font-family: system-ui, -apple-system, sans-serif !important;
    }
    
    @media (min-width: 768px) {
        .response-section textarea {
            min-height: 220px !important;
            font-size: 16px !important;
            padding: 20px !important;
        }
    }
    
    @media (min-width: 1200px) {
        .response-section textarea {
            min-height: 250px !important;
            font-size: 17px !important;
        }
    }
    
    /* Button styling - mobile touch friendly but more compact */
    .main-action-btn {
        background: linear-gradient(45deg, #ff6b6b, #feca57) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: bold !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        width: 100% !important;
        min-height: 44px !important; /* Touch-friendly but compact */
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
        transition: all 0.3s ease !important;
    }
    
    @media (min-width: 768px) {
        .main-action-btn {
            font-size: 16px !important;
            padding: 14px 20px !important;
            min-height: 48px !important;
        }
    }
    
    .main-action-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    .secondary-btn {
        background: linear-gradient(45deg, #4ecdc4, #45b7d1) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 10px 16px !important;
        margin: 6px 0 !important;
        width: 100% !important;
        min-height: 40px !important; /* More compact */
        transition: all 0.3s ease !important;
    }
    
    @media (min-width: 768px) {
        .secondary-btn {
            font-size: 15px !important;
            padding: 12px 20px !important;
            min-height: 44px !important;
        }
    }
    
    .secondary-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Utility buttons - very small corner icons */
    .util-btn {
        border-radius: 50% !important;
        padding: 4px !important;
        min-width: 24px !important;
        min-height: 24px !important;
        font-size: 12px !important;
        border: 1px solid #ccc !important;
        background: rgba(255,255,255,0.9) !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
        position: absolute !important;
        z-index: 10 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    @media (min-width: 768px) {
        .util-btn {
            min-width: 28px !important;
            min-height: 28px !important;
            font-size: 14px !important;
            padding: 6px !important;
        }
    }
    
    .util-btn:hover {
        background: #ff6b6b !important;
        color: white !important;
        border-color: #ff6b6b !important;
        transform: scale(1.1) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }
    
    /* Corner positioning for utility buttons */
    .corner-top-right {
        top: 8px !important;
        right: 8px !important;
    }
    
    .corner-top-left {
        top: 8px !important;
        left: 8px !important;
    }
    
    .corner-bottom-right {
        bottom: 8px !important;
        right: 8px !important;
    }
    
    /* Text container positioning */
    .text-container {
        position: relative !important;
        display: inline-block !important;
        width: 100% !important;
    }
    
    /* Language section */
    .language-section {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 12px;
        padding: 12px;
        margin: 12px 0;
    }
    
    @media (min-width: 768px) {
        .language-section {
            border-radius: 15px;
            padding: 15px;
            margin: 15px 0;
        }
    }
    
    /* Instructions styling */
    .instructions {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        font-size: 14px;
    }
    
    @media (min-width: 768px) {
        .instructions {
            border-radius: 15px;
            padding: 20px;
            font-size: 15px;
        }
    }
    
    /* Conversation section */
    .conversation-section {
        margin-top: 15px;
        border-top: 2px solid #f0f0f0;
        padding-top: 15px;
    }
    
    /* Mobile-specific optimizations */
    @media (max-width: 767px) {
        /* Reduce margins on mobile */
        .block {
            margin: 8px 0 !important;
        }
        
        /* Ensure text is readable */
        label {
            font-size: 14px !important;
        }
        
        /* Make dropdowns mobile friendly and compact */
        select {
            font-size: 15px !important;
            padding: 10px !important;
            border-radius: 8px !important;
        }
        
        /* Accordion headers */
        .accordion-header {
            font-size: 15px !important;
            padding: 12px !important;
        }
    }
    
    /* Prevent horizontal scroll on mobile */
    .overflow-hidden {
        overflow-x: hidden !important;
    }
    
    /* Loading states */
    .loading {
        opacity: 0.7;
        pointer-events: none;
    }
    """
) as demo:
    
    # Main title
    gr.HTML('<h1 class="main-title">🎨 KnowKidDraw - AI Art Gallery! 🌈</h1>')
    
    # Instructions section - mobile optimized
    with gr.Accordion("📖 How to Use (Tap to expand)", open=False, elem_classes="instructions"):
        gr.Markdown("""
        ### Welcome Young Artists! 🎭
        
        **Simple Steps for Parents & Kids:**
        1. 🤖 **Choose AI Art Appreciator** (cloud or local)
        2. 📸 **Click x on the right corner of gif box, then upload artwork** or use examples  
        3. 💭 **Describe the drawing** (optional)
        4. ✨ **Tap magic button** for AI response
        5. 💬 **Ask follow-up questions**
        6. 🌍 **You can choose to translate the response to other languages**
        
        **Perfect for:**
        - 👨‍👩‍👧‍👦 Family art time on phones/tablets
        - 🏫 Teachers with student artwork
        - 🎨 Young artists learning other feels about their creations
        """)
    
    # Model Selection Section - mobile optimized
    with gr.Group(elem_classes="model-selection"):
        gr.Markdown("### 🤖 I am your Art Appreciator")
        with gr.Group(elem_classes="text-container"):
            model_dropdown = gr.Dropdown(
                choices=get_model_choices(),
                label="Choose an AI Personality",
                value=get_model_choices()[0],
                container=False,
                elem_id="model_select"
            )
            refresh_button = gr.Button("🔄", elem_classes="util-btn corner-top-right", elem_id="refresh")
    
    # Large Image Display Section - responsive
    with gr.Group(elem_classes="image-section"):
        image_input = gr.Image(
            type="filepath",
            label="🎨 Upload Your Amazing Artwork",
            value=get_example_gif(),
            height=300,  # Responsive via CSS
            width="100%",
            interactive=True,  # Enable upload functionality
            show_label=True,
            show_download_button=False,
            elem_id="image_upload"
        )
    
    # Input Question Section - with corner microphone
    with gr.Group(elem_classes="input-section"):
        with gr.Group(elem_classes="text-container"):
            initial_q = gr.Textbox(
                label="💭 Tell me about your drawing",
                placeholder="Leave blank for a surprise, or tell me about your artwork...",
                lines=2,
                elem_id="initial_question"
            )
            mic_button = gr.Button("🎤", elem_classes="util-btn corner-top-right", elem_id="mic1")
    
    # Main Action Button - touch friendly
    draw_button = gr.Button("✨ Show Me The Magic! ✨", elem_classes="main-action-btn")
    
    # Response Area - with corner speaker button
    with gr.Group(elem_classes="response-section"):
        with gr.Group(elem_classes="text-container"):
            art_output = gr.Textbox(
                label="🎭 Your Art Story", 
                lines=8,  # Responsive via CSS
                placeholder="Your AI art critic's wonderful response will appear here...",
                elem_id="art_response"
            )
            speaker_button = gr.Button("🔊", elem_classes="util-btn corner-top-right", elem_id="speaker")
    
    # Follow-up Conversation Section
    with gr.Group(elem_classes="conversation-section"):
        gr.Markdown("### 💬 Ask More Questions")
        with gr.Group(elem_classes="text-container"):
            followup_q = gr.Textbox(
                label="Continue the conversation",
                placeholder="What else would you like to know?",
                lines=2,
                elem_id="followup_question"
            )
            mic_button2 = gr.Button("🎤", elem_classes="util-btn corner-top-right", elem_id="mic2")
        
        followup_button = gr.Button("💬 Tell Me More", elem_classes="secondary-btn")
    
    # Language & Translation Section
    with gr.Group(elem_classes="language-section"):
        gr.Markdown("### 🌍 Language")
        with gr.Group(elem_classes="text-container"):
            language_dropdown = gr.Dropdown(
                choices=[
                    "English", 
                    "Traditional Chinese (繁體中文) - Coming Soon", 
                    "Simplified Chinese (简体中文) - Coming Soon"
                ],
                label="Choose Language",
                value="English",
                elem_id="language_select"
            )
            translate_button = gr.Button("🌐", elem_classes="util-btn corner-top-right", elem_id="translate")
    
    # Action Buttons - mobile friendly
    clear_button = gr.Button("🔄 Try Another Drawing", elem_classes="secondary-btn")
    
    # Hidden status field
    speech_status = gr.Textbox(visible=False)
    
    # Event Handlers
    
    # Model refresh
    refresh_button.click(
        fn=refresh_models,
        inputs=[],
        outputs=[model_dropdown]
    )
    
    # Main analysis with better error handling
    def analyze_with_feedback(image_path, initial_q, model_choice):
        """Wrapper function to provide user feedback during processing"""
        if image_path is None:
            return "Please upload your amazing artwork! 🎨"
        
        # Show processing message
        try:
            return kid_draw_analysis(image_path, initial_q, model_choice)
        except Exception as e:
            return f"Oops! There was an error processing your artwork: {str(e)}. Please try again! 🎨"
    
    draw_button.click(
        fn=analyze_with_feedback,
        inputs=[image_input, initial_q, model_dropdown],
        outputs=[art_output],
        show_progress=True  # Show progress indicator
    )
    
    # Follow-up analysis
    followup_button.click(
        fn=follow_up_analysis,
        inputs=[image_input, art_output, followup_q, model_dropdown],
        outputs=[art_output]
    ).then(
        fn=lambda: "",  # Clear the followup question field
        inputs=[],
        outputs=[followup_q]
    )
    
    # Reset interface
    def reset_interface():
        new_image = get_example_gif() if os.path.exists("Example.gif") else get_random_example()
        return new_image, "", "", ""
    
    clear_button.click(
        fn=reset_interface,
        inputs=[],
        outputs=[image_input, initial_q, art_output, followup_q]
    )
    
    # Translation
    translate_button.click(
        fn=translate_text_libre,
        inputs=[art_output, language_dropdown],
        outputs=[art_output]
    )
    
    # Microphone placeholders
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
    
    # Speaker placeholder
    speaker_button.click(
        fn=text_to_speech_placeholder,
        inputs=[],
        outputs=[speech_status]
    )

if __name__ == "__main__":
    demo.launch(
        share=False,
        inbrowser=True,
        show_error=True
    )
