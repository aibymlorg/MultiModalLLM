# MultModalLLM

**A First Trail in Multi-Modal LLM**

A comprehensive multimodal AI application built with Gradio and powered by Llama 3.2 Vision models through Together AI. This application demonstrates various computer vision and multimodal AI capabilities across different use cases.

## 🚀 Features

### 🏠 Interior Design Analysis
- Upload interior design images for detailed analysis
- Get insights on design style, color schemes, materials, and furniture
- Ask follow-up questions for deeper analysis
- Perfect for interior designers and homeowners

### 🧾 Receipt Reading & Analysis  
- Process multiple receipt images simultaneously
- Extract key information like totals, items, and dates
- Calculate summary totals across multiple receipts
- Ideal for expense tracking and accounting

### 📊 Graph to Table Conversion
- Convert charts, graphs, and visualizations to HTML tables
- Extract data points from visual representations
- Export structured data for further analysis
- Useful for data analysis and reporting

## 🛠️ Technology Stack

- **Frontend**: Gradio web interface
- **AI Model**: Llama 3.2 Vision (90B) via Together AI
- **Image Processing**: PIL, base64 encoding
- **Backend**: Python 3.10+
- **Dependencies**: PyTorch, NumPy, Matplotlib

## 📋 Prerequisites

- Python 3.10 or higher
- Together AI API key
- pip package manager

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aibymlorg-2124/MultModalLLM.git
   cd MultModalLLM
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   TOGETHER_API_KEY=your_together_ai_api_key_here
   ```

## 🚀 Running the Application

### Main Application
```bash
python app.py
```

### Alternative Interfaces
```bash
# Gradio interface
python gradio-app.py

# Local version
python local_app.py

# Chatbot interface  
python chatbot.py
```

The application will start a local web server (usually at `http://localhost:7860`) where you can interact with the multimodal AI features.

## 📁 Project Structure

```
MultModalLLM/
├── 📄 Main Application Files
│   ├── app.py                    # Main Gradio app (Llama3.2-vision-90B)
│   ├── utils.py                  # Utility functions for AI models
│   ├── gradio-app.py            # Alternative Gradio interface
│   ├── local_app.py             # Local version of the app
│   └── chatbot.py               # Chatbot functionality
│
├── 🔧 Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # API keys (create this file)
│   └── .gitignore              # Git ignore rules
│
├── 📚 Learning Materials
│   └── MultiModal_LLamaLesson/  # Tutorial lessons and examples
│
├── 🗂️ Other Projects
│   ├── MemoryLaneHK/           # Memory Lane HK project
│   ├── kiddrawai/              # Kid Draw AI project
│   └── Experiment/             # Experimental code
│
└── 🖼️ Assets
    └── Various sample images and receipts
```

## 🔧 Configuration

### Together AI Setup
1. Sign up at [Together AI](https://together.ai/)
2. Get your API key from the dashboard
3. Add it to your `.env` file

### Model Configuration
The application uses Llama 3.2 Vision models. You can modify the model size in `utils.py`:
- `11B-Vision-Instruct-Turbo` (default)
- `90B-Vision-Instruct-Turbo` (for better performance)

## 🎯 Usage Examples

### Interior Design Analysis
1. Navigate to the "Interior Design" tab
2. Upload an interior image
3. Enter your question or use the default prompt
4. Click "Analyze Interior" for results

### Receipt Processing
1. Go to the "Read Receipts" tab  
2. Upload one or multiple receipt images
3. Customize the analysis questions
4. Get itemized and summary analysis

### Graph Conversion
1. Open the "Graph to Table" tab
2. Upload a chart or graph image
3. Specify conversion requirements
4. Get HTML table output

## 🚀 Deployment

### Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Local Development
```bash
# Run with auto-reload
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📝 API Keys Required

- **Together AI**: For Llama 3.2 Vision model access
- **Optional**: Wolfram Alpha API key for mathematical computations

## 🐛 Troubleshooting

### Common Issues
1. **API Key Error**: Ensure your Together AI API key is correctly set in `.env`
2. **Image Upload Issues**: Check image format (JPG, PNG supported)
3. **Memory Issues**: Use smaller model size (11B instead of 90B)

### Performance Tips
- Use smaller images for faster processing
- Batch multiple receipts for efficiency
- Clear browser cache if interface issues occur

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Together AI for providing access to Llama 3.2 Vision models
- Gradio team for the excellent web interface framework
- Meta for developing the Llama model family

## 📞 Support

For questions and support:
- Create an issue on GitHub
- Contact: aibyml.org@gmail.com

---

**Built with ❤️ using Claude Code**