import gradio as gr
import requests
import json

# Available models with correct Ollama model names
AVAILABLE_MODELS = {
    "llama": "llama3.1:latest",
    "deepseek": "deepseek-r1:32b",
    "qwq": "qwq:latest"
}

# Ollama API endpoints
OLLAMA_BASE_URL = "http://localhost:11434/api"
CHAT_ENDPOINT = f"{OLLAMA_BASE_URL}/chat"

def generate_streaming_response(prompt, conversation_history, model_name="llama3.1:latest"):
    """Generate streaming response for general chat"""
    messages = []
    for human, assistant in conversation_history:
        messages.extend([
            {"role": "user", "content": human},
            {"role": "assistant", "content": assistant}
        ])
    
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": True
    }
    
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'message' in json_response and 'content' in json_response['message']:
                    yield json_response['message']['content']
                
    except requests.exceptions.RequestException as e:
        yield f"Error: {str(e)}\nMake sure Ollama is running and the model is installed."

def chat_respond(message, chat_history, model_choice):
    """Handle chat responses with streaming"""
    model_name = AVAILABLE_MODELS[model_choice.lower().replace(" 3.1", "")]
    chat_history = chat_history + [(message, "")]
    yield "", chat_history
    
    current_response = ""
    for chunk in generate_streaming_response(message, chat_history[:-1], model_name):
        current_response += chunk
        chat_history[-1] = (message, current_response)
        yield "", chat_history

# [Previous functions remain unchanged]
[... Keep all the previous functions for story creation ...]

# Create Gradio interface
with gr.Blocks(title="AI Story Creation & Chat") as demo:
    gr.Markdown("# 🤖 AI Story Creation & Chat")
    
    with gr.Tabs() as tabs:
        # Chat Tab
        with gr.Tab("Simple Chat"):
            with gr.Column():
                chat_model_choice = gr.Dropdown(
                    choices=["Llama 3.1", "Deepseek R1", "QWQ"],
                    label="Choose Model",
                    value="Llama 3.1",
                    info="Select the AI model for chat"
                )
                chatbox = gr.Chatbot(
                    height=600,
                    show_label=False,
                    bubble_full_width=False
                )
                msg = gr.Textbox(
                    label="Type your message here...",
                    placeholder="Type your message here...",
                    show_label=False
                )
                clear_chat = gr.ClearButton([msg, chatbox])

                # Connect chat components
                msg.submit(
                    chat_respond,
                    inputs=[msg, chatbox, chat_model_choice],
                    outputs=[msg, chatbox]
                )
        
        # Story Creation Tab
        with gr.Tab("Story Creation"):
            with gr.Row():
                with gr.Column(scale=1):
                    name_input = gr.Textbox(label="Your Name (optional)")
                    culture_input = gr.Textbox(
                        label="Culture",
                        placeholder="e.g., Chinese, Japanese, Western"
                    )
                    language_input = gr.Textbox(
                        label="Language",
                        placeholder="e.g., English, Chinese, Japanese"
                    )
                    content_input = gr.Textbox(
                        label="Story Content",
                        lines=3,
                        placeholder="Enter your story content here"
                    )
                    model_choice = gr.Dropdown(
                        choices=["Llama 3.1", "Deepseek R1", "QWQ"],
                        label="Choose Model",
                        value="Llama 3.1",
                        info="Select the AI model to use"
                    )
                    
                    with gr.Row():
                        create_btn = gr.Button("Create Story", variant="primary")
                        compare_btn = gr.Button("Compare Models")
                    
                    edit_input = gr.Textbox(
                        label="Edit Instructions",
                        lines=2,
                        placeholder="Enter your editing instructions here"
                    )
                    edit_btn = gr.Button("Edit Story")

                with gr.Column(scale=2):
                    story_chatbot = gr.Chatbot(
                        height=600,
                        show_label=False,
                        bubble_full_width=False
                    )
                    clear_story = gr.ClearButton([story_chatbot])

                # Connect story components
                create_btn.click(
                    create_story,
                    inputs=[name_input, culture_input, language_input, content_input, model_choice, story_chatbot],
                    outputs=[edit_input, story_chatbot]
                )
                
                edit_btn.click(
                    edit_story,
                    inputs=[edit_input, story_chatbot, model_choice],
                    outputs=[edit_input, story_chatbot]
                )
                
                compare_btn.click(
                    compare_models,
                    inputs=[name_input, culture_input, language_input, content_input, story_chatbot],
                    outputs=[edit_input, story_chatbot]
                )

    gr.Markdown("""
    ### Model Information:
    - Llama 3.1: 8B parameters, fast (~1 min response)
    - Deepseek R1: 32B parameters, thorough but slower (~5 min)
    - QWQ: 32B parameters, thorough but slower (~5 min)
    
    ### Note:
    - Chat tab: Have a normal conversation with the AI
    - Story Creation tab: Create and edit stories with cultural adaptation
    """)

if __name__ == "__main__":
    print("Starting AI Story Creation & Chat... Please ensure Ollama is running.")
    demo.launch(server_name="0.0.0.0", share=True)