import { NextRequest, NextResponse } from 'next/server';
import { analyzeWithImage, callAI } from '@/lib/ai-provider';
import { AIProvider } from '@/types/api';

export async function POST(request: NextRequest) {
  try {
    const { images, provider } = await request.json();

    if (!images || !Array.isArray(images) || images.length === 0) {
      return NextResponse.json(
        { error: 'No images provided' },
        { status: 400 }
      );
    }

    const results = [];
    let totalResponse = '';
    let usedProvider: AIProvider = 'llama';

    for (const image of images) {
      const response = await analyzeWithImage(
        "What's the total charge in the receipt?",
        image,
        90,
        provider as AIProvider
      );
      results.push(response.result);
      totalResponse += `${response.result}\n`;
      usedProvider = response.provider;
    }

    const totalResponse2 = await callAI(
      `What's the total charge of all the receipts below?\n${totalResponse}`,
      provider as AIProvider
    );

    const finalResult = `Individual Receipts:\n${totalResponse}\nTotal Analysis:\n${totalResponse2.result}`;

    return NextResponse.json({ 
      result: finalResult,
      provider: totalResponse2.provider 
    });
  } catch (error) {
    console.error('Receipt analysis error:', error);
    return NextResponse.json(
      { error: 'Failed to analyze receipts' },
      { status: 500 }
    );
  }
}