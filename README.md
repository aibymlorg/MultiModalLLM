# Multimodal LLama Analysis - Next.js TypeScript

A modern web application for AI-powered image analysis using Llama 3.2 Vision model, converted from the original Python Gradio application.

## Features

- **Interior Design Analysis**: Analyze interior design elements, styles, and objects in images
- **Receipt Reading**: Extract and calculate totals from multiple receipt images
- **Graph to Table**: Convert charts and graphs into HTML tables

## Tech Stack

- **Frontend**: Next.js 14+ with TypeScript
- **Styling**: Tailwind CSS
- **File Upload**: react-dropzone
- **AI Model**: Llama 3.2 Vision via Together AI API
- **Image Processing**: Sharp (server-side)

## Setup Instructions

### 1. Environment Variables

Configure your API keys in `.env.local`:

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

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## AI Provider Support

The application supports multiple AI providers with automatic fallback:

### Supported Providers
- **Llama 3.2 Vision** (via Together AI) - Primary provider for multimodal analysis
- **Gemini 1.5 Flash** (via Google AI) - Fallback provider with excellent vision capabilities

### How It Works
1. **Automatic Selection**: The app chooses the best available provider based on your configuration
2. **Smart Fallback**: If the primary provider fails, it automatically tries the fallback provider
3. **Provider Priority**: Configure which provider to try first via `AI_PROVIDER_PRIORITY`
4. **Real-time Status**: See which provider is being used in the UI

### Configuration Options
- Set `AI_PROVIDER_PRIORITY=llama,gemini` to prefer Llama first
- Set `AI_PROVIDER_PRIORITY=gemini,llama` to prefer Gemini first
- Configure only one API key to use a single provider

## API Endpoints

- `POST /api/interior-design` - Analyze interior design images
- `POST /api/receipts` - Process multiple receipt images  
- `POST /api/graph-to-table` - Convert graphs to HTML tables
- `GET /api/providers` - Get available provider information

## Usage

1. **Interior Design Tab**: Upload an interior image to get detailed analysis of design elements, materials, and objects
2. **Receipts Tab**: Upload multiple receipt images to extract totals and get a combined analysis
3. **Graph to Table Tab**: Upload chart/graph images to convert them into structured HTML tables
4. **Provider Selection**: Switch between available AI providers or let the app choose automatically

## Project Structure

```
src/
├── app/
│   ├── api/           # API routes
│   └── page.tsx       # Main application page
├── components/        # React components
├── lib/              # Utility functions
└── types/            # TypeScript type definitions
```

## Differences from Python Version

- **Modern UI**: Replaced Gradio with custom React components
- **Better UX**: Drag & drop file uploads, real-time previews
- **Type Safety**: Full TypeScript implementation
- **Performance**: Optimized image handling and API calls
- **Deployment Ready**: Built for modern hosting platforms

## Deployment

The application is ready to deploy on platforms like:

- [Vercel](https://vercel.com) (recommended)
- [Netlify](https://netlify.com)
- [Railway](https://railway.app)

Make sure to configure your environment variables in the deployment platform.
