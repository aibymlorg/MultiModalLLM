import React, { useState, useRef, useEffect } from 'react';
import { Pencil, Eraser, RotateCcw, Save, MessageCircle, Mic, Image, Sticker, Rainbow } from 'lucide-react';

const UnifiedDrawingInterface = () => {
  const [showWelcome, setShowWelcome] = useState(true);

  useEffect(() => {
    setTimeout(() => setShowWelcome(false), 3000);
  }, []);
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [tool, setTool] = useState('pencil');
  const [color, setColor] = useState('#000000');
  const [brushSize, setBrushSize] = useState(5);
  const [isListening, setIsListening] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [voiceCommand, setVoiceCommand] = useState('');

  // Stickers and stamps
  const stickers = [
    { id: 'star', emoji: '⭐' },
    { id: 'heart', emoji: '❤️' },
    { id: 'sun', emoji: '☀️' },
    { id: 'tree', emoji: '🌳' },
    { id: 'flower', emoji: '🌸' },
    { id: 'rainbow', emoji: '🌈' },
  ];

  const brushSizes = [
    { size: 3, name: 'Small' },
    { size: 8, name: 'Medium' },
    { size: 15, name: 'Large' },
  ];

  const colors = [
    { hex: '#FF6B6B', name: 'Red' },
    { hex: '#4ECDC4', name: 'Turquoise' },
    { hex: '#FFD93D', name: 'Yellow' },
    { hex: '#95E1D3', name: 'Mint' },
    { hex: '#FF8B94', name: 'Pink' },
    { hex: '#6C5CE7', name: 'Purple' },
    { hex: '#A8E6CF', name: 'Light Green' },
    { hex: '#FDCB6E', name: 'Orange' },
  ];

  const startVoiceRecognition = () => {
    setIsListening(true);
    // Mock voice recognition - replace with actual API
    setTimeout(() => {
      setVoiceCommand("I want to draw a rainbow!");
      setIsListening(false);
      // Mock Llama response
      setAnalysis({
        description: "That's a wonderful idea! Let's draw a rainbow together. Would you like to use the rainbow colors?",
        suggestion: "Try using these colors in order: red, orange, yellow, green, blue, purple!",
        mood: "excited"
      });
    }, 2000);
  };

  const addSticker = (emoji) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.font = '30px Arial';
    ctx.fillText(emoji, Math.random() * (canvas.width - 50), Math.random() * (canvas.height - 50));
  };

  return (
    <div className="flex flex-col p-6 bg-gray-50 min-h-screen">
      {showWelcome && (
        <div className="fixed inset-0 bg-purple-600 flex items-center justify-center z-50">
          <div className="text-center text-white">
            <div className="text-8xl mb-4">🎨</div>
            <h1 className="text-6xl font-bold mb-2">KidDraw AI</h1>
            <p className="text-2xl">Let's create something amazing!</p>
          </div>
        </div>
      )}
      
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <div className="text-4xl">🎨</div>
          <h1 className="text-3xl font-bold text-purple-600">KidDraw AI</h1>
        </div>
      </div>
      <div className="bg-white rounded-xl p-4 mb-6 shadow-lg">
        <div className="flex flex-wrap gap-6 justify-between">
          {/* Color Palette */}
          <div className="flex flex-wrap gap-3">
            {colors.map((c) => (
              <button
                key={c.hex}
                className={`w-12 h-12 rounded-xl transition-transform hover:scale-110 
                  ${color === c.hex ? 'ring-4 ring-blue-400 transform scale-110' : ''}`}
                style={{ backgroundColor: c.hex }}
                onClick={() => setColor(c.hex)}
                title={c.name}
              />
            ))}
          </div>

          {/* Brush Sizes */}
          <div className="flex gap-3">
            {brushSizes.map((b) => (
              <button
                key={b.size}
                className={`p-2 rounded-lg ${brushSize === b.size ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
                onClick={() => setBrushSize(b.size)}
              >
                <div 
                  className="rounded-full bg-current"
                  style={{ width: b.size * 2, height: b.size * 2 }}
                />
              </button>
            ))}
          </div>
        </div>

        {/* Tools */}
        <div className="flex gap-4 mt-4">
          <button
            className={`p-4 rounded-xl ${tool === 'pencil' ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
            onClick={() => setTool('pencil')}
          >
            <Pencil className="w-6 h-6" />
          </button>
          <button
            className={`p-4 rounded-xl ${tool === 'eraser' ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
            onClick={() => setTool('eraser')}
          >
            <Eraser className="w-6 h-6" />
          </button>
          <button
            className={`p-4 rounded-xl ${tool === 'rainbow' ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
            onClick={() => setTool('rainbow')}
          >
            <Rainbow className="w-6 h-6" />
          </button>
          <div className="border-r border-gray-200 mx-2" />
          {/* Stickers */}
          <div className="flex gap-2">
            {stickers.map((sticker) => (
              <button
                key={sticker.id}
                className="p-2 text-2xl hover:scale-110 transition-transform"
                onClick={() => addSticker(sticker.emoji)}
              >
                {sticker.emoji}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex gap-6">
        <div className="flex-1">
          <canvas
            ref={canvasRef}
            width={800}
            height={600}
            className="w-full bg-white rounded-xl shadow-lg"
          />
        </div>

        <div className="w-96 bg-white p-6 rounded-xl shadow-lg">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-purple-600">AI Friend</h2>
            <button
              onClick={startVoiceRecognition}
              className={`p-4 rounded-full ${isListening ? 'bg-red-500' : 'bg-purple-500'} text-white`}
            >
              <Mic className="w-6 h-6" />
            </button>
          </div>

          {voiceCommand && (
            <div className="mb-4 p-3 bg-purple-50 rounded-lg">
              <p className="text-sm italic">"{voiceCommand}"</p>
            </div>
          )}

          {analysis && (
            <div className="space-y-4">
              <div className="p-4 bg-purple-50 rounded-lg">
                <MessageCircle className="w-6 h-6 text-purple-500 mb-2" />
                <p className="text-sm leading-relaxed">{analysis.description}</p>
              </div>
              
              {analysis.suggestion && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm font-medium text-blue-800">{analysis.suggestion}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UnifiedDrawingInterface;