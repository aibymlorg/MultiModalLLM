import { LlamaMessage, LlamaResponse, ApiError } from '@/types/api';

const TOGETHER_API_BASE = process.env.DLAI_TOGETHER_API_BASE || 'https://api.together.xyz';
const TOGETHER_API_KEY = process.env.TOGETHER_API_KEY;

export async function callLlama(
  messages: LlamaMessage[],
  modelSize: number = 11
): Promise<string> {
  if (!TOGETHER_API_KEY) {
    throw new Error('TOGETHER_API_KEY is not configured');
  }

  const model = `meta-llama/Llama-3.2-${modelSize}B-Vision-Instruct-Turbo`;
  const url = `${TOGETHER_API_BASE}/v1/chat/completions`;

  const payload = {
    model,
    max_tokens: 4096,
    temperature: 0.0,
    stop: ["<|eot_id|>", "<|eom_id|>"],
    messages
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${TOGETHER_API_KEY}`
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result: LlamaResponse | ApiError = await response.json();

  if ('error' in result) {
    throw new Error(result.error);
  }

  return result.choices[0].message.content;
}

export async function analyzeWithImage(
  prompt: string,
  imageBase64: string,
  modelSize: number = 90
): Promise<string> {
  const messages: LlamaMessage[] = [
    {
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: imageBase64 } }
      ]
    }
  ];

  return await callLlama(messages, modelSize);
}

export async function followUpAnalysis(
  initialPrompt: string,
  imageBase64: string,
  initialResult: string,
  followUpPrompt: string,
  modelSize: number = 90
): Promise<string> {
  const messages: LlamaMessage[] = [
    {
      role: 'user',
      content: [
        { type: 'text', text: initialPrompt },
        { type: 'image_url', image_url: { url: imageBase64 } }
      ]
    },
    {
      role: 'assistant',
      content: initialResult
    },
    {
      role: 'user',
      content: followUpPrompt
    }
  ];

  return await callLlama(messages, modelSize);
}