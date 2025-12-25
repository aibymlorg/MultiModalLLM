import gradio as gr
import time
import random
import os
import requests
import json
import base64
import io
from PIL import Image
import warnings
from utils import load_env, llama32, llama31, disp_image, merge_images, resize_image

warnings.filterwarnings('ignore')
load_env()

# Available AI models using cloud APIs (Together.ai)
AVAILABLE_MODELS = {
    "llama-vision": "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    "llama-text": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    "llama-text-70b": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
}

MODEL_CONFIG = {
    "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo": {
        "supports_vision": True,
        "max_tokens": 4096,
        "temperature": 0.1,
        "use_for": ["photo_analysis", "visual_context"]
    },
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": {
        "supports_vision": False,
        "max_tokens": 8192,
        "temperature": 0.1,
        "use_for": ["story_generation", "refinement"]
    },
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": {
        "supports_vision": False,
        "max_tokens": 4096,
        "temperature": 0.1,
        "use_for": ["story_generation", "creative_writing"]
    }
}

# Default content for demonstration purposes
DEFAULT_STORYBOARD = """## Storyboard Created: 4 Scenes

### Scene 1:
- **Narration:** "My first day of high school was a symphony of butterflies and possibilities. The imposing redbrick building loomed before me, its corridors stretching like labyrinths compared to the cozy confines of my middle school."
- **Visual:** School photo 1 with nostalgic filter
- **Music:** Gentle ambient music reflecting early 2000s era

### Scene 2:
- **Narration:** "The cafeteria at noon was a sociological experiment – hundreds of teenagers instinctively sorting themselves into tribal tables. I stood frozen, lunch tray gripped with white knuckles, until I heard someone call my name."
- **Visual:** School photo 2 with nostalgic filter
- **Music:** Soft piano underscoring the moment of connection

### Scene 3:
- **Narration:** "Mr. Peterson, with his Einstein-wild hair and bow tie slightly askew, stood behind a cluttered desk with the focused expression of a mad scientist. Without introduction, he combined liquids from two beakers..."
- **Visual:** School photo 3 with nostalgic filter
- **Music:** Playful, curious melody with science-lab inspired sounds

### Scene 4:
- **Narration:** "Those seemingly ordinary moments became the first brushstrokes on the canvas of my adolescence. What I couldn't appreciate then, but see with perfect clarity now..."
- **Visual:** School photo 1 transitioning gradually to present day
- **Music:** Emotional crescendo reflecting personal growth and nostalgia
"""

# Memory Photo Analysis Functions using cloud APIs
def encode_image_for_llama(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        raise Exception(f"Error encoding image: {str(e)}")

def process_image_for_llama(image_path, prompt):
    """
    Process image and create message structure for llama32 cloud API
    
    Args:
        image_path (str): Path to the image file
        prompt (str): Text prompt for the model
    
    Returns:
        str: Model response
    """
    try:
        if not os.path.exists(image_path):
            return "Error: Image file not found"
            
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
        
        response = llama32(messages)
        return response if response else "No response received from model"
        
    except Exception as e:
        return f"Error processing image: {str(e)}"

def memory_photos(image_path, initial_question, followup_question):
    """
    Analyze Memory Photos image with custom questions using cloud API
    """
    if image_path is None:
        return "Please upload an image."
    
    if not initial_question.strip():
        initial_question = ("Describe what is in the photos, seasons, scene, animal and human "
                          "aspects of the emotions of persons in this photo. Then list all "
                          "the objects in the photo.")
    
    # First analysis
    result = process_image_for_llama(image_path, initial_question)
    
    if result.startswith("Error"):
        return result
    
    # Follow-up analysis if provided
    if followup_question.strip():
        try:
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
            return f"Initial Analysis:\n{result}\n\nFollow-up Analysis:\n{final_result}"
        except Exception as e:
            return f"{result}\n\nError in follow-up analysis: {str(e)}"
    
    return result

def check_system_status():
    """Check if cloud APIs are properly configured"""
    try:
        # Check if required environment variables are set
        required_vars = ["TOGETHER_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return f"❌ Missing environment variables: {', '.join(missing_vars)}"
        
        # Test a simple API call
        test_messages = [{"role": "user", "content": "Hello, test connection"}]
        test_response = llama31(test_messages)
        
        if test_response:
            return f"✅ Cloud API connection successful!\n🔧 Available models: {list(AVAILABLE_MODELS.keys())}\n📡 Using Together.ai API"
        else:
            return "❌ Cloud API connection failed"
            
    except Exception as e:
        return f"❌ Error checking system status: {str(e)}"

# Existing storyboard and video functions
def create_storyboard(story_text, uploaded_images):
    """Creates a storyboard from story text and images"""
    time.sleep(2)  # Simulate processing time
    
    if not story_text.strip():
        return "Please provide analysis results first before creating a storyboard."
    
    # Use default storyboard if no images uploaded
    if not uploaded_images:
        return DEFAULT_STORYBOARD + "\n\n*Note: Upload photos to create a personalized storyboard with your actual images.*"
    
    # Count paragraphs as scenes
    paragraphs = [p.strip() for p in story_text.split("\n\n") if p.strip()]
    scene_count = min(len(paragraphs), len(uploaded_images))
    
    if scene_count == 0:
        return DEFAULT_STORYBOARD
    
    storyboard = f"## Storyboard Created: {scene_count} Scenes\n\n"
    
    for i, paragraph in enumerate(paragraphs[:scene_count], 1):
        storyboard += f"### Scene {i}:\n"
        storyboard += f"- **Narration:** \"{paragraph[:150]}{'...' if len(paragraph) > 150 else ''}\"\n"
        storyboard += f"- **Visual:** Photo {i} with enhanced lighting and effects\n"
        storyboard += f"- **Music:** Ambient music matching the emotional tone\n\n"
    
    if len(paragraphs) > scene_count:
        storyboard += f"### Additional Content:\n"
        storyboard += f"*{len(paragraphs) - scene_count} more memory elements detected. Upload more photos to include additional scenes.*\n\n"
    
    return storyboard

def preview_video(storyboard_text, uploaded_images):
    """Generates video creation preview based on storyboard and images"""
    time.sleep(3)  # Simulate processing time

    if not isinstance(storyboard_text, str) or not storyboard_text.strip():
        return "Please create a storyboard first before generating video preview."
    
    if "Please provide analysis results" in storyboard_text:
        return "Please create a storyboard first before generating video preview."

    image_count = len(uploaded_images) if uploaded_images else 0
    
    video_description = f"""
# Video Preview Generated

## Video Specifications:
- **Duration:** {2 + (image_count * 0.3):.1f} minutes
- **Resolution:** 1080p HD
- **Style:** Nostalgic memory presentation with smooth transitions
- **Images Used:** {image_count} photos
- **Scenes:** {storyboard_text.count('### Scene')} memory scenes

## 🎯 What to Expect:
- **AI-Generated Narration:** Warm, nostalgic voice reading your memory analysis
- **Visual Enhancement:** Vintage filters and gentle animations
- **Dynamic Music:** Background soundtrack matching emotional content
- **Smooth Transitions:** Gentle effects bringing memories to life
- **Emotional Pacing:** Timing optimized for reflection and nostalgia

## 🎵 Audio Features:
- Warm, personal narration voice
- Background music that complements emotional journey
- Sound effects for transitions and highlights
- Professional audio mixing with nostalgic tone

## 🎨 Visual Effects:
- Vintage, warm color grading
- Gentle image animations (pan, zoom, fade)
- Text overlays for key memories
- Smooth, dreamy scene transitions

## 📱 Export Options:
- MP4 format for easy sharing
- Multiple resolution options (720p, 1080p, 4K)
- Social media optimized versions
- Direct sharing to platforms

---
*In a full implementation, you would see an interactive preview player here with options to customize narration style, music selection, and visual effects before finalizing your memory video.*

**[Preview would begin with a gentle fade-in to your first image, accompanied by nostalgic music as your memory narration begins...]**
"""
    
    return video_description

def update_progress(step):
    """Updates the progress indicator"""
    progress = {
        "analysis": 0, 
        "storyboard": 0, 
        "video": 0,
        "current_step": step
    }
    
    if step == "analysis":
        progress["analysis"] = 100
    elif step == "storyboard":
        progress["analysis"] = 100
        progress["storyboard"] = 100
    elif step == "video":
        progress["analysis"] = 100
        progress["storyboard"] = 100
        progress["video"] = 100
        
    return progress

# Main application
with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"), title="Memory Lane") as app:
    
    # Global state variables
    current_analysis = gr.State("")
    current_storyboard = gr.State("")
    current_images = gr.State([])
    
    # Header
    with gr.Row():
        gr.Markdown("# 🔍 Memory Lane")
        with gr.Column(scale=1, min_width=200):
            gr.Markdown("*Powered by Cloud AI Vision Models*")
    
    # Navigation Tabs
    with gr.Tabs() as tabs:
        analysis_tab = gr.Tab("🔍 My Memory")
        storyboard_tab = gr.Tab("🎬 Storyboard")  
        video_tab = gr.Tab("🎥 Video Creation")
        dashboard_tab = gr.Tab("📊 Dashboard")
    
    # Dashboard Tab Content
    with dashboard_tab:
        gr.Markdown("## 🚀 What was in the photos?")
        
        # System status section
        with gr.Row():
            status_button = gr.Button("Check System Status", variant="secondary")
            status_output = gr.Textbox(label="System Status", interactive=False)
        
        status_button.click(fn=check_system_status, outputs=status_output)
        
        # Progress indicators
        progress_status = gr.JSON(
            value={
                "analysis": 0, 
                "storyboard": 0, 
                "video": 0,
                "current_step": "none"
            },
            label="Project Progress",
            visible=False
        )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🔍 Analysis Progress")
                analysis_progress = gr.Slider(
                    minimum=0, 
                    maximum=100, 
                    value=0, 
                    label="Analysis Progress",
                    interactive=False
                )
            
            with gr.Column():
                gr.Markdown("### 🎭 Storyboard Creation")
                storyboard_progress = gr.Slider(
                    minimum=0, 
                    maximum=100, 
                    value=0, 
                    label="Storyboard Progress",
                    interactive=False
                )
            
            with gr.Column():
                gr.Markdown("### 🎬 Video Creation")
                video_progress = gr.Slider(
                    minimum=0, 
                    maximum=100, 
                    value=0, 
                    label="Video Progress",
                    interactive=False
                )
        
        # Project overview
        gr.Markdown("""
        ## 🎯 How It Works:
        
        **1. 🔍 Memory Analysis** - Upload images and analyze them with AI:
        - **Memory Photos**: Analyze seasons, places, emotions, and aesthetics
            
        **2. 🎬 Create a Storyboard** - Transform your analysis into a structured visual narrative
        
        **3. 🎥 Generate Video** - Create a professional presentation video from your memories
        
        *Navigate to the tabs above to work through each phase of your memory project.*
        """)
    
    # Memory Analysis Tab
    with analysis_tab:
        gr.Markdown("# 🔍 Begin walking along your memory lane")
        
        with gr.Tab("💭 Memory Context"):
            initial_q = gr.Textbox(
                label="Something you treasure from your past", 
                placeholder="Describe the scene, seasons, place, person...",
                value="Tell me something about what you want to remember and cherish ..."
            )
            if initial_q:
                gr.Markdown("# 🔍 Do you have some photos")
                
        with gr.Tab("📸 Memory Photos"):
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(type="filepath", label="Upload Memorable Photos")
                    photo_button = gr.Button("Recall from Memory Photos, (please press once)", variant="primary")
                with gr.Column():
                    photo_recall = gr.Textbox(label="Memory from the photos ...", lines=15, max_lines=25)
                    
        with gr.Tab("🤔 More about the memory"):
            with gr.Column():
                followup_q = gr.Textbox(
                    label="Follow-up Question (Optional)",
                    placeholder="Ask a follow-up question based on the initial analysis",
                    value="Tell me more about the emotions and relationships visible in this photo"
                )
            
            photo_button.click(
                fn=memory_photos, 
                inputs=[image_input, initial_q, followup_q], 
                outputs=photo_recall
        )
        
            # Save Analysis Results
            with gr.Column():
                save_analysis_btn = gr.Button("💾 Save the Memory & Continue to Storyboard", variant="primary")
    
    # Storyboard Tab Content
    with storyboard_tab:
        gr.Markdown("## 🎬 Create Your Memory Storyboard")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📝 Your Memory Analysis")
                storyboard_analysis_display = gr.Textbox(
                    lines=8,
                    label="Analysis Content",
                    interactive=False,
                    placeholder="Complete memory analysis in the previous tab to see results here"
                )
 
            with gr.Column():
                gr.Markdown("### 📷 Your Memory Images")
                storyboard_photos_display = gr.Gallery(
                    label="Memory Images from Previous Tab",
                    show_label=True,
                    columns=2,
                    rows=2,
                    height="auto",
                    value=None,
                    interactive=False
                )
                
                gr.Markdown("*Images from your analysis will appear here automatically*")     

        create_storyboard_btn = gr.Button("🎭 Create Storyboard from Memory & Images", variant="primary")
        
        storyboard_output = gr.Markdown(
            label="Your Memory Storyboard",
            value="*Create your storyboard by completing analysis and clicking the button above*"
        )
        
        storyboard_save_btn = gr.Button("💾 Save Storyboard & Continue to Video", variant="primary")
    
    # Video Creation Tab Content
    with video_tab:
        gr.Markdown("## 🎥 Generate Your Memory Video")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 🎬 Your Memory Storyboard")
                video_storyboard_display = gr.Markdown(
                    value="*Complete the storyboard in the previous tab to see it here*"
                )
            
            with gr.Column():
                gr.Markdown("### 📸 Your Memory Images")
                video_photos_display = gr.Gallery(
                    label="Memory Images",
                    show_label=True,
                    elem_id="video_gallery",
                    columns=2,
                    rows=2,
                    height="auto"
                )
        
        generate_video_btn = gr.Button("🎬 Generate Memory Video", variant="primary", size="lg")
        
        video_preview = gr.Markdown(
            label="Video Preview",
            value="*Generate your video using the button above*"
        )
        
        with gr.Row():
            video_download_btn = gr.Button("📱 Download Memory Video", variant="secondary")
            share_btn = gr.Button("🔗 Share Video", variant="secondary")
    
    # Event Handlers
    def save_analysis_results(memory_recall):
        """Save analysis results from memory analysis"""
        combined_analysis = ""
        
        if memory_recall and memory_recall.strip() and memory_recall != "Please upload an image.":
            combined_analysis += f"## Memory Photos Analysis:\n{memory_recall}\n\n"
             
        if not combined_analysis:
            combined_analysis = "No analysis results to save. Please complete memory analysis first."
        
        status = update_progress("analysis")
        return combined_analysis, combined_analysis, status

    def collect_all_images(image1):
        """Collect all uploaded images from analysis tabs"""
        images = []
        
        if image1:
            images.append(image1)
        
        return images

    def create_and_save_storyboard(analysis, images):
        if not analysis.strip() or "No analysis results" in analysis:
            return "Please complete memory analysis first.", "", [], update_progress("none")
            
        storyboard = create_storyboard(analysis, images)
        status = update_progress("storyboard")
        return storyboard, storyboard, images or [], status

    def update_video_tab_display(storyboard, images):
        return storyboard, images or []

    def generate_video_and_update(storyboard, photos):
        if not storyboard.strip() or "Please complete analysis" in storyboard:
            return "Please create a storyboard first.", update_progress("none")
            
        video = preview_video(storyboard, photos)
        status = update_progress("video")
        return video, status

    def update_progress_ui(progress_data):
        return (
            progress_data["analysis"], 
            progress_data["storyboard"],
            progress_data["video"]
        )

    # Connect event handlers
    save_analysis_btn.click(
        fn=save_analysis_results,
        inputs=[photo_recall],
        outputs=[storyboard_analysis_display, current_analysis, progress_status]
    )

    # Collect images from analysis tab
    save_analysis_btn.click(
        fn=collect_all_images,
        inputs=[image_input],
        outputs=[storyboard_photos_display]
    )

    create_storyboard_btn.click(
        fn=create_and_save_storyboard,
        inputs=[storyboard_analysis_display, storyboard_photos_display],
        outputs=[storyboard_output, current_storyboard, current_images, progress_status]
    )

    storyboard_save_btn.click(
        fn=update_video_tab_display,
        inputs=[current_storyboard, current_images],
        outputs=[video_storyboard_display, video_photos_display]
    )

    generate_video_btn.click(
        fn=generate_video_and_update,
        inputs=[video_storyboard_display, current_images],
        outputs=[video_preview, progress_status]
    )

    progress_status.change(
        fn=update_progress_ui,
        inputs=progress_status,
        outputs=[analysis_progress, storyboard_progress, video_progress]
    )

    video_download_btn.click(lambda: gr.Info("Video download would start here!"))
    share_btn.click(lambda: gr.Info("Sharing options would appear here!"))

    # Load initial status
    app.load(fn=check_system_status, outputs=status_output)

# Launch the application
if __name__ == "__main__":
    print("🚀 Starting Memory Lane Application...")
    print("🔍 Testing cloud API availability...")
    
    # Test API availability
    status = check_system_status()
    print(f"✅ System status: {status}")
    
    print("🌐 Launching application for HuggingFace Spaces...")
    app.launch(
        share=False,  # HuggingFace handles sharing
        debug=False   # Disable debug for production
    )