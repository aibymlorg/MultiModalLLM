import React, { useState, useRef, useEffect } from 'react';
import { Pencil, Eraser, RotateCcw, Save, Send, Mic } from 'lucide-react';

const DrawingInterface = () => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [tool, setTool] = useState('pencil');
  const [color, setColor] = useState('#000000');
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  
  // Drawing functions remain the same...
  
  const analyzePicture = async () => {
    const canvas = canvasRef.current;
    const imageData = canvas.toDataURL('image/png');
    
    // Mock Llama-3.2 response - replace with actual API call
    const mockResponse = {
      analysis: "I see you've drawn a lovely house with a tree! The bright colors suggest happy feelings. Would you like to tell me more about who lives there?",
      sentiment: "positive",
      suggestedPrompts: ["Tell me about the people in the house", "What's your favorite part of the drawing?"]
    };
    
    setMessages(prev => [...prev, 
      { type: 'image', content: imageData },
      { type: 'ai', content: mockResponse.analysis }
    ]);
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;
    
    setMessages(prev => [...prev, { type: 'user', content: userInput }]);
    setUserInput('');
    
    // Mock Llama response - replace with actual API call
    const mockAIResponse = "That's interesting! I notice you used bright colors. How were you feeling when you drew this?";
    setTimeout(() => {
      setMessages(prev => [...prev, { type: 'ai', content: mockAIResponse }]);
    }, 1000);
  };

  return (
    <div className="flex gap-4 p-4 bg-gray-100 h-screen">
      <div className="flex flex-col w-2/3">
        {/* Drawing tools */}
        <div className="mb-4 flex gap-2">
          {/* Previous drawing tools code */}
        </div>
        
        <canvas
          ref={canvasRef}
          width={600}
          height={400}
          className="bg-white border-2 border-gray-300 rounded-lg"
          // Previous canvas event handlers
        />
      </div>

      <div className="w-1/3 flex flex-col bg-white rounded-lg p-4">
        <div className="flex-grow overflow-y-auto mb-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`mb-2 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
              {msg.type === 'image' ? (
                <img src={msg.content} alt="drawing" className="max-w-xs rounded" />
              ) : (
                <div className={`inline-block p-2 rounded-lg ${
                  msg.type === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'
                }`}>
                  {msg.content}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <button
            onClick={analyzePicture}
            className="p-2 rounded bg-purple-500 text-white"
          >
            Analyze Drawing
          </button>
          <button className="p-2 rounded bg-blue-500 text-white">
            <Mic className="w-6 h-6" />
          </button>
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            className="flex-grow p-2 border rounded"
            placeholder="Tell me about your drawing..."
          />
          <button
            onClick={sendMessage}
            className="p-2 rounded bg-green-500 text-white"
          >
            <Send className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default DrawingInterface;