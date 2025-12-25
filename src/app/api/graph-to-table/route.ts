import { NextRequest, NextResponse } from 'next/server';
import { analyzeWithImage } from '@/lib/ai-provider';
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

    const response = await analyzeWithImage(
      "Convert the chart to an HTML table.",
      image,
      90,
      provider as AIProvider
    );

    return NextResponse.json({ 
      result: response.result,
      provider: response.provider 
    });
  } catch (error) {
    console.error('Graph to table analysis error:', error);
    return NextResponse.json(
      { error: 'Failed to convert graph to table' },
      { status: 500 }
    );
  }
}