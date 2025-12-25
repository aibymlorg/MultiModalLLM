'use client';

import { useState } from 'react';
import FileUpload from './FileUpload';
import ProviderStatus from './ProviderStatus';
import { AIProvider } from '@/types/api';

export default function ReceiptsTab() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [previewUrls, setPreviewUrls] = useState<string[]>([]);
  const [currentProvider, setCurrentProvider] = useState<AIProvider | undefined>();

  const handleFileSelect = (files: File[]) => {
    setSelectedFiles(files);
    setPreviewUrls(files.map(file => URL.createObjectURL(file)));
    setResult('');
  };

  const convertFilesToBase64 = async (files: File[]): Promise<string[]> => {
    const promises = files.map(file => {
      return new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = error => reject(error);
      });
    });

    return Promise.all(promises);
  };

  const handleAnalyze = async () => {
    if (selectedFiles.length === 0) return;

    setLoading(true);
    try {
      const base64Images = await convertFilesToBase64(selectedFiles);
      
      const response = await fetch('/api/receipts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ images: base64Images, provider: currentProvider }),
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
          <h3 className="text-lg font-semibold">Receipt Analysis</h3>
          <ProviderStatus 
            currentProvider={currentProvider} 
            onProviderChange={setCurrentProvider}
          />
        </div>
        <FileUpload 
          onFileSelect={handleFileSelect} 
          multiple={true}
        />
      </div>

      {previewUrls.length > 0 && (
        <div>
          <h4 className="font-medium mb-2">Previews ({selectedFiles.length} files):</h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {previewUrls.map((url, index) => (
              <div key={index} className="relative">
                <img
                  src={url}
                  alt={`Receipt ${index + 1}`}
                  className="w-full h-32 object-cover rounded-lg shadow-md"
                />
                <div className="absolute top-2 left-2 bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded">
                  {index + 1}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={handleAnalyze}
        disabled={selectedFiles.length === 0 || loading}
        className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Analyzing Receipts...' : `Analyze ${selectedFiles.length} Receipt${selectedFiles.length !== 1 ? 's' : ''}`}
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