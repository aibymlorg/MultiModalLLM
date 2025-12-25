'use client';

import { useState } from 'react';
import FileUpload from './FileUpload';
import ProviderStatus from './ProviderStatus';
import { AIProvider } from '@/types/api';

export default function InteriorDesignTab() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [currentProvider, setCurrentProvider] = useState<AIProvider | undefined>();

  const handleFileSelect = (files: File[]) => {
    if (files.length > 0) {
      const file = files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult('');
    }
  };

  const convertFileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = error => reject(error);
    });
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    try {
      const base64Image = await convertFileToBase64(selectedFile);
      
      const response = await fetch('/api/interior-design', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: base64Image, provider: currentProvider }),
      });

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      setResult(data.result);
      setCurrentProvider(data.provider);
    } catch (error) {
      console.error('Analysis failed:', error);
      setResult(`Error: ${error instanceof Error ? error.message : 'Analysis failed'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Interior Design Analysis</h3>
          <ProviderStatus 
            currentProvider={currentProvider} 
            onProviderChange={setCurrentProvider}
          />
        </div>
        <FileUpload onFileSelect={handleFileSelect} />
      </div>

      {previewUrl && (
        <div>
          <h4 className="font-medium mb-2">Preview:</h4>
          <img
            src={previewUrl}
            alt="Preview"
            className="max-w-full max-h-64 rounded-lg shadow-md"
          />
        </div>
      )}

      <button
        onClick={handleAnalyze}
        disabled={!selectedFile || loading}
        className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Analyzing...' : 'Analyze Interior'}
      </button>

      {result && (
        <div>
          <h4 className="font-medium mb-2">Analysis Result:</h4>
          <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap text-sm">
            {result}
          </div>
        </div>
      )}
    </div>
  );
}