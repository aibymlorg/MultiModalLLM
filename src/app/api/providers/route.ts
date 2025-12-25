import { NextRequest, NextResponse } from 'next/server';
import { getAvailableProviders, getProviderPriority } from '@/lib/ai-provider';

export async function GET(request: NextRequest) {
  try {
    const providers = getAvailableProviders();
    const priority = getProviderPriority();

    return NextResponse.json({ 
      providers,
      priority,
      recommended: priority.find(p => providers.find(prov => prov.name === p && prov.available)) || null
    });
  } catch (error) {
    console.error('Provider info error:', error);
    return NextResponse.json(
      { error: 'Failed to get provider information' },
      { status: 500 }
    );
  }
}