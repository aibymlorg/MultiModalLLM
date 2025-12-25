import { AIProvider, AIProviderConfig } from '@/types/api';
import { callLlama, analyzeWithImage as analyzeWithImageLlama, followUpAnalysis as followUpAnalysisLlama } from './llama';
import { callGemini, analyzeWithImageGemini, followUpAnalysisGemini, isGeminiAvailable } from './gemini';

function isLlamaAvailable(): boolean {
  return !!(process.env.TOGETHER_API_KEY);
}

export function getAvailableProviders(): AIProviderConfig[] {
  const providers: AIProviderConfig[] = [];

  if (isLlamaAvailable()) {
    providers.push({ name: 'llama', available: true });
  } else {
    providers.push({ name: 'llama', available: false, error: 'TOGETHER_API_KEY not configured' });
  }

  if (isGeminiAvailable()) {
    providers.push({ name: 'gemini', available: true });
  } else {
    providers.push({ name: 'gemini', available: false, error: 'GEMINI_API_KEY not configured' });
  }

  return providers;
}

export function getProviderPriority(): AIProvider[] {
  const priority = process.env.AI_PROVIDER_PRIORITY || 'llama,gemini';
  return priority.split(',').map(p => p.trim() as AIProvider);
}

export function selectProvider(preferredProvider?: AIProvider): AIProvider {
  const providers = getAvailableProviders();
  const priority = getProviderPriority();

  if (preferredProvider) {
    const provider = providers.find(p => p.name === preferredProvider && p.available);
    if (provider) {
      return preferredProvider;
    }
  }

  for (const providerName of priority) {
    const provider = providers.find(p => p.name === providerName && p.available);
    if (provider) {
      return providerName as AIProvider;
    }
  }

  throw new Error('No AI providers are available. Please configure TOGETHER_API_KEY or GEMINI_API_KEY.');
}

export async function analyzeWithImage(
  prompt: string,
  imageBase64: string,
  modelSize: number = 90,
  preferredProvider?: AIProvider
): Promise<{ result: string; provider: AIProvider }> {
  const provider = selectProvider(preferredProvider);

  try {
    let result: string;
    
    if (provider === 'gemini') {
      result = await analyzeWithImageGemini(prompt, imageBase64);
    } else {
      result = await analyzeWithImageLlama(prompt, imageBase64, modelSize);
    }

    return { result, provider };
  } catch (error) {
    console.error(`${provider} analysis failed:`, error);
    
    const fallbackProviders = getProviderPriority().filter(p => p !== provider);
    for (const fallbackProvider of fallbackProviders) {
      const providers = getAvailableProviders();
      const providerConfig = providers.find(p => p.name === fallbackProvider && p.available);
      
      if (providerConfig) {
        try {
          console.log(`Falling back to ${fallbackProvider}`);
          let result: string;
          
          if (fallbackProvider === 'gemini') {
            result = await analyzeWithImageGemini(prompt, imageBase64);
          } else {
            result = await analyzeWithImageLlama(prompt, imageBase64, modelSize);
          }

          return { result, provider: fallbackProvider };
        } catch (fallbackError) {
          console.error(`${fallbackProvider} fallback failed:`, fallbackError);
          continue;
        }
      }
    }

    throw error;
  }
}

export async function followUpAnalysis(
  initialPrompt: string,
  imageBase64: string,
  initialResult: string,
  followUpPrompt: string,
  modelSize: number = 90,
  preferredProvider?: AIProvider
): Promise<{ result: string; provider: AIProvider }> {
  const provider = selectProvider(preferredProvider);

  try {
    let result: string;
    
    if (provider === 'gemini') {
      result = await followUpAnalysisGemini(initialPrompt, imageBase64, initialResult, followUpPrompt);
    } else {
      result = await followUpAnalysisLlama(initialPrompt, imageBase64, initialResult, followUpPrompt, modelSize);
    }

    return { result, provider };
  } catch (error) {
    console.error(`${provider} follow-up analysis failed:`, error);
    
    const fallbackProviders = getProviderPriority().filter(p => p !== provider);
    for (const fallbackProvider of fallbackProviders) {
      const providers = getAvailableProviders();
      const providerConfig = providers.find(p => p.name === fallbackProvider && p.available);
      
      if (providerConfig) {
        try {
          console.log(`Falling back to ${fallbackProvider} for follow-up`);
          let result: string;
          
          if (fallbackProvider === 'gemini') {
            result = await followUpAnalysisGemini(initialPrompt, imageBase64, initialResult, followUpPrompt);
          } else {
            result = await followUpAnalysisLlama(initialPrompt, imageBase64, initialResult, followUpPrompt, modelSize);
          }

          return { result, provider: fallbackProvider };
        } catch (fallbackError) {
          console.error(`${fallbackProvider} follow-up fallback failed:`, fallbackError);
          continue;
        }
      }
    }

    throw error;
  }
}

export async function callAI(
  prompt: string,
  preferredProvider?: AIProvider
): Promise<{ result: string; provider: AIProvider }> {
  const provider = selectProvider(preferredProvider);

  try {
    let result: string;
    
    if (provider === 'gemini') {
      result = await callGemini(prompt);
    } else {
      const messages = [{ role: 'user' as const, content: prompt }];
      result = await callLlama(messages);
    }

    return { result, provider };
  } catch (error) {
    console.error(`${provider} call failed:`, error);
    
    const fallbackProviders = getProviderPriority().filter(p => p !== provider);
    for (const fallbackProvider of fallbackProviders) {
      const providers = getAvailableProviders();
      const providerConfig = providers.find(p => p.name === fallbackProvider && p.available);
      
      if (providerConfig) {
        try {
          console.log(`Falling back to ${fallbackProvider}`);
          let result: string;
          
          if (fallbackProvider === 'gemini') {
            result = await callGemini(prompt);
          } else {
            const messages = [{ role: 'user' as const, content: prompt }];
            result = await callLlama(messages);
          }

          return { result, provider: fallbackProvider };
        } catch (fallbackError) {
          console.error(`${fallbackProvider} fallback failed:`, fallbackError);
          continue;
        }
      }
    }

    throw error;
  }
}