import React, { useState } from 'react';
import { Pencil, Eraser } from 'lucide-react';

const DrawingApp = () => {
  const [selectedColor, setSelectedColor] = useState('#F87171');
  const [selectedTool, setSelectedTool] = useState('pencil');

  const colors = [
    '#F87171', // coral
    '#6EE7B7', // mint
    '#FDE68A', // yellow
    '#A7F3D0', // light green
    '#FCA5A5', // light red
    '#818CF8', // purple
    '#A7F3D0', // mint green
    '#FCD34D', // gold
  ];

  const tools = [
    { id: 'pencil', icon: <Pencil className="w-6 h-6" /> },
    { id: 'eraser', icon: <Eraser className="w-6 h-6" /> },
  ];

  const stickers = ['⭐', '❤️', '☀️', '🌳', '🌸', '🌈'];

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm p-4">
        <div className="flex items-center gap-2">
          <div className="text-4xl">🎨</div>
          <h1 className="text-3xl font-bold text-purple-600">KidDraw AI</h1>
        </div>
      </header>

      <main className="flex-1 p-4">
        <div className="flex gap-4">
          {/* Tools Panel */}
          <div className="bg-white rounded-lg shadow-md p-4 flex flex-col gap-4">
            {tools.map((tool) => (
              <button
                key={tool.id}
                className={`p-3 rounded-lg ${
                  selectedTool === tool.id
                    ? 'bg-purple-100 text-purple-600'
                    : 'hover:bg-gray-100'
                }`}
                onClick={() => setSelectedTool(tool.id)}
              >
                {tool.icon}
              </button>
            ))}
          </div>

          {/* Color Palette */}
          <div className="bg-white rounded-lg shadow-md p-4 flex flex-wrap gap-2">
            {colors.map((color) => (
              <button
                key={color}
                className={`w-12 h-12 rounded-lg transition-transform ${
                  selectedColor === color ? 'scale-110 ring-2 ring-purple-600' : ''
                }`}
                style={{ backgroundColor: color }}
                onClick={() => setSelectedColor(color)}
              />
            ))}
          </div>

          {/* Stickers */}
          <div className="bg-white rounded-lg shadow-md p-4 flex flex-wrap gap-2">
            {stickers.map((sticker) => (
              <button
                key={sticker}
                className="w-12 h-12 text-2xl flex items-center justify-center hover:bg-gray-100 rounded-lg"
              >
                {sticker}
              </button>
            ))}
          </div>
        </div>

        {/* Canvas Area */}
        <div className="mt-4 bg-white rounded-lg shadow-md aspect-video">
          <DrawingCanvas color={selectedColor} tool={selectedTool} />
        </div>
      </main>
    </div>
  );
};

export default DrawingApp;