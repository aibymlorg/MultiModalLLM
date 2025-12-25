import { NextRequest, NextResponse } from 'next/server';
import { analyzeWithImage, followUpAnalysis } from '@/lib/ai-provider';
import { AIProvider } from '@/types/api';

export async function POST(request: NextRequest) {
  try {
    const { image, provider } = await request.json();

    if (!image) {
      return NextResponse.json(
        { error: 'No image provided' },
        { status: 400 }
      );
    }

    const initialPrompt = "Describe the design, style, color, material and other aspects of the fireplace in this photo. Then list all the objects in the photo.";
    
    const initialResponse = await analyzeWithImage(initialPrompt, image, 90, provider as AIProvider);
    
    const followUpPrompt = "How many balls and vases are there? Which one is closer to the fireplace: the balls or the vases?";
    
    const finalResponse = await followUpAnalysis(
      initialPrompt,
      image,
      initialResponse.result,
      followUpPrompt,
      90,
      provider as AIProvider
    );

    const combinedResult = `${initialResponse.result}\n\nAdditional Analysis:\n${finalResponse.result}`;

    return NextResponse.json({ 
      result: combinedResult,
      provider: finalResponse.provider 
    });
  } catch (error) {
    console.error('Interior design analysis error:', error);
    return NextResponse.json(
      { error: 'Failed to analyze interior design' },
      { status: 500 }
    );
  }
}