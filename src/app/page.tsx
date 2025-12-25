'use client';

import { useState } from 'react';
import InteriorDesignTab from '@/components/InteriorDesignTab';
import ReceiptsTab from '@/components/ReceiptsTab';
import GraphToTableTab from '@/components/GraphToTableTab';

type TabType = 'interior' | 'receipts' | 'graph';

export default function Home() {
  const [activeTab, setActiveTab] = useState<TabType>('interior');

  const tabs = [
    { id: 'interior' as const, label: 'Interior Design', component: InteriorDesignTab },
    { id: 'receipts' as const, label: 'Read Receipts', component: ReceiptsTab },
    { id: 'graph' as const, label: 'Graph to Table', component: GraphToTableTab },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
              <h1 className="text-3xl font-bold">Multimodal LLama Analysis</h1>
              <p className="mt-2 opacity-90">AI-powered image analysis and data extraction</p>
            </div>

            {/* Tab Navigation */}
            <div className="border-b border-gray-200">
              <div className="flex">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                      activeTab === tab.id
                        ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Tab Content */}
            <div className="p-6">
              {tabs.map((tab) => {
                const Component = tab.component;
                return (
                  <div
                    key={tab.id}
                    className={activeTab === tab.id ? 'block' : 'hidden'}
                  >
                    <Component />
                  </div>
                );
              })}
            </div>
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-gray-600 text-sm">
            <p>Powered by Llama 3.2 Vision • Built with Next.js & TypeScript</p>
          </div>
        </div>
      </div>
    </div>
  );
}
