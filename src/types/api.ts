export type AIProvider = 'llama' | 'gemini';

export interface LlamaMessage {
  role: 'user' | 'assistant';
  content: string | Array<{
    type: 'text' | 'image_url';
    text?: string;
    image_url?: {
      url: string;
    };
  }>;
}

export interface LlamaResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

export interface GeminiPart {
  text?: string;
  inlineData?: {
    mimeType: string;
    data: string;
  };
}

export interface GeminiContent {
  parts: GeminiPart[];
}

export interface ApiError {
  error: string;
}

export interface AnalysisRequest {
  prompt: string;
  image?: string;
  modelSize?: number;
  provider?: AIProvider;
}

export interface ReceiptAnalysisRequest {
  images: string[];
  provider?: AIProvider;
}

export interface GraphAnalysisRequest {
  image: string;
  provider?: AIProvider;
}

export interface AIProviderConfig {
  name: string;
  available: boolean;
  error?: string;
}