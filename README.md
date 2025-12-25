# MultiModalLLM - Next.js TypeScript Implementation

**Modern Multi-Modal LLM Web Application**

A modern, production-ready web application for AI-powered image analysis, converted from Python Gradio to Next.js TypeScript with dual AI provider support.

## 🚀 Key Features

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

### Next.js Version (This Implementation)
- **Frontend**: Next.js 14+ with TypeScript
- **Styling**: Tailwind CSS
- **File Upload**: react-dropzone
- **AI Providers**: Llama 3.2 Vision & Gemini 1.5 Flash
- **Image Processing**: Sharp (server-side)
- **Type Safety**: Full TypeScript implementation

### Legacy Python Version (Also Available)
- **Frontend**: Gradio web interface
- **AI Model**: Llama 3.2 Vision (90B) via Together AI
- **Backend**: Python 3.10+
- **Dependencies**: PyTorch, NumPy, Matplotlib

## 🤖 AI Provider Support

The Next.js application supports multiple AI providers with intelligent fallback:

### Supported Providers
- **Llama 3.2 Vision** (via Together AI) - Primary provider for multimodal analysis
- **Gemini 1.5 Flash** (via Google AI) - Fallback provider with excellent vision capabilities

### How It Works
1. **Automatic Selection**: The app chooses the best available provider based on your configuration
2. **Smart Fallback**: If the primary provider fails, it automatically tries the fallback provider
3. **Provider Priority**: Configure which provider to try first via `AI_PROVIDER_PRIORITY`
4. **Real-time Status**: See which provider is being used in the UI

## ⚙️ Setup Instructions

### Next.js Application Setup

1. **Navigate to the Next.js app:**
   ```bash
   cd multimodal-llm-nextjs
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   Create `.env.local` with your API keys:
   ```env
   # AI Provider Configuration
   TOGETHER_API_KEY=your_together_api_key_here
   DLAI_TOGETHER_API_BASE=https://api.together.xyz
   GEMINI_API_KEY=your_gemini_api_key_here

   # Optional APIs
   WOLFRAM_ALPHA_KEY=your_wolfram_alpha_key_here
   TAVILY_API_KEY=your_tavily_api_key_here

   # Provider Priority (comma-separated: llama,gemini or gemini,llama)
   AI_PROVIDER_PRIORITY=llama,gemini
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Python Application Setup (Legacy)

1. **Navigate to Python lessons:**
   ```bash
   cd MultiModal_LLamaLesson
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Python app:**
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
MultiModalLLM/
├── 📱 Next.js Implementation
│   └── multimodal-llm-nextjs/
│       ├── src/
│       │   ├── app/api/          # API routes
│       │   ├── components/       # React components
│       │   ├── lib/             # AI provider logic
│       │   └── types/           # TypeScript definitions
│       ├── package.json
│       └── README.md
│
├── 🐍 Python Implementation
│   └── MultiModal_LLamaLesson/
│       ├── app.py               # Main Gradio app
│       ├── utils.py             # Utility functions
│       └── requirements.txt
│
├── 🗂️ Other Projects
│   ├── MemoryLaneHK/           # Memory Lane HK project
│   ├── kiddrawai/              # Kid Draw AI project
│   └── Experiment/             # Experimental code
│
└── 📄 Main Files
    ├── app.py                   # Original Gradio app
    ├── requirements.txt         # Python dependencies
    └── utils.py                 # Shared utilities
```

## 🌐 API Endpoints (Next.js)

- `POST /api/interior-design` - Analyze interior design images
- `POST /api/receipts` - Process multiple receipt images  
- `POST /api/graph-to-table` - Convert graphs to HTML tables
- `GET /api/providers` - Get available provider information

## 🎯 Usage Examples

### Next.js Application
1. **Interior Design Tab**: Upload images, select AI provider, get detailed analysis
2. **Receipts Tab**: Upload multiple receipts, get itemized and summary totals
3. **Graph to Table Tab**: Convert charts to structured HTML tables
4. **Provider Selection**: Switch between Llama and Gemini or let the app choose automatically

### Python Application
1. Navigate to specific tabs in the Gradio interface
2. Upload images using the file upload component
3. Use default prompts or customize your questions
4. Get AI-powered analysis results

## 🚀 Deployment

### Next.js Deployment
- **Vercel** (recommended): Connect your GitHub repository
- **Netlify**: Deploy with environment variables
- **Railway**: Full-stack deployment with database support

### Python Deployment
- **Gradio Cloud**: Direct deployment from Python code
- **Hugging Face Spaces**: Free hosting for Gradio apps
- **Local**: Run with `python app.py`

## 🔧 Configuration Options

### AI Provider Priority (Next.js)
- `AI_PROVIDER_PRIORITY=llama,gemini` - Prefer Llama first
- `AI_PROVIDER_PRIORITY=gemini,llama` - Prefer Gemini first
- Configure only one API key to use a single provider

### Model Configuration (Python)
- `11B-Vision-Instruct-Turbo` (default)
- `90B-Vision-Instruct-Turbo` (for better performance)

## 🔑 API Keys Required

- **Together AI**: For Llama 3.2 Vision model access
- **Google AI**: For Gemini 1.5 Flash model access
- **Optional**: Wolfram Alpha API key for mathematical computations

## 🆚 Next.js vs Python Comparison

| Feature | Next.js | Python/Gradio |
|---------|---------|---------------|
| **UI/UX** | Modern React components | Gradio interface |
| **Type Safety** | Full TypeScript | Python typing |
| **Deployment** | Vercel, Netlify | Gradio Cloud, HF Spaces |
| **AI Providers** | Dual provider support | Single provider |
| **Performance** | Optimized builds | Python runtime |
| **Customization** | Highly customizable | Gradio limitations |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Together AI for providing access to Llama 3.2 Vision models
- Google AI for Gemini API access
- Next.js team for the excellent React framework
- Gradio team for the Python interface framework
- Meta for developing the Llama model family

## 📞 Support

For questions and support:
- Create an issue on GitHub
- Contact: aibyml.org@gmail.com

---

**Built with ❤️ using Claude Code**
