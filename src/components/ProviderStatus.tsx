'use client';

import { useEffect, useState } from 'react';
import { AIProvider, AIProviderConfig } from '@/types/api';

interface ProviderInfo {
  providers: AIProviderConfig[];
  priority: AIProvider[];
  recommended: AIProvider | null;
}

interface ProviderStatusProps {
  currentProvider?: AIProvider;
  onProviderChange?: (provider: AIProvider) => void;
}

export default function ProviderStatus({ currentProvider, onProviderChange }: ProviderStatusProps) {
  const [providerInfo, setProviderInfo] = useState<ProviderInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProviderInfo = async () => {
      try {
        const response = await fetch('/api/providers');
        const data = await response.json();
        setProviderInfo(data);
      } catch (error) {
        console.error('Failed to fetch provider info:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProviderInfo();
  }, []);

  if (loading || !providerInfo) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
        <span>Loading providers...</span>
      </div>
    );
  }

  const availableProviders = providerInfo.providers.filter(p => p.available);
  const getProviderDisplayName = (provider: string) => {
    switch (provider) {
      case 'llama': return 'Llama 3.2';
      case 'gemini': return 'Gemini 1.5';
      default: return provider;
    }
  };

  const getProviderColor = (provider: string) => {
    switch (provider) {
      case 'llama': return 'text-blue-600';
      case 'gemini': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="flex items-center gap-4 text-sm">
      {/* Current Provider Status */}
      {currentProvider && (
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${currentProvider === 'llama' ? 'bg-blue-500' : 'bg-green-500'}`}></div>
          <span className="text-gray-600">Using:</span>
          <span className={`font-medium ${getProviderColor(currentProvider)}`}>
            {getProviderDisplayName(currentProvider)}
          </span>
        </div>
      )}

      {/* Provider Selector */}
      {onProviderChange && availableProviders.length > 1 && (
        <div className="flex items-center gap-2">
          <span className="text-gray-500">Switch to:</span>
          <div className="flex gap-1">
            {availableProviders.map((provider) => (
              <button
                key={provider.name}
                onClick={() => onProviderChange(provider.name as AIProvider)}
                className={`px-2 py-1 rounded text-xs transition-colors ${
                  currentProvider === provider.name
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                }`}
                disabled={currentProvider === provider.name}
              >
                {getProviderDisplayName(provider.name)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Available Providers Count */}
      <div className="text-gray-400 text-xs">
        {availableProviders.length} of {providerInfo.providers.length} providers available
      </div>
    </div>
  );
}