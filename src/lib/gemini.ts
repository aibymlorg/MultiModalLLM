import { GoogleGenerativeAI, Part } from '@google/generative-ai';

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

let genAI: GoogleGenerativeAI | null = null;

if (GEMINI_API_KEY) {
  genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
}

export async function callGemini(
  prompt: string,
  imageBase64?: string,
  model: string = 'gemini-1.5-flash'
): Promise<string> {
  if (!genAI || !GEMINI_API_KEY) {
    throw new Error('Gemini API key is not configured');
  }

  const generativeModel = genAI.getGenerativeModel({ model });

  const parts: Part[] = [{ text: prompt }];

  if (imageBase64) {
    const base64Data = imageBase64.replace(/^data:image\/[a-z]+;base64,/, '');
    const mimeType = imageBase64.match(/data:([a-zA-Z0-9]+\/[a-zA-Z0-9-.+]+)/)?.[1] || 'image/jpeg';
    
    parts.push({
      inlineData: {
        mimeType,
        data: base64Data
      }
    });
  }

  try {
    const result = await generativeModel.generateContent(parts);
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error('Gemini API error:', error);
    throw new Error(`Gemini API failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export async function analyzeWithImageGemini(
  prompt: string,
  imageBase64: string
): Promise<string> {
  return await callGemini(prompt, imageBase64);
}

export async function followUpAnalysisGemini(
  initialPrompt: string,
  imageBase64: string,
  initialResult: string,
  followUpPrompt: string
): Promise<string> {
  const combinedPrompt = `
Previous analysis:
Prompt: ${initialPrompt}
Result: ${initialResult}

Follow-up question: ${followUpPrompt}

Please answer the follow-up question based on the image and the previous analysis context.
  `;

  return await callGemini(combinedPrompt, imageBase64);
}

export function isGeminiAvailable(): boolean {
  return !!(GEMINI_API_KEY && genAI);
}