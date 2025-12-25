import React, { useState } from 'react';
import { Bell, AlertTriangle, Calendar, Heart, Brain, TrendingUp, MessageCircle } from 'lucide-react';

const ParentDashboard = () => {
  const [selectedTimeframe, setTimeframe] = useState('week');
  const [showAlert, setShowAlert] = useState(true);

  const mockChildData = {
    name: "Alex",
    age: 7,
    recentDrawings: [
      {
        id: 1,
        date: "2025-01-22",
        analysis: {
          mood: "content",
          engagement: "high",
          patterns: ["social interaction", "family focus"],
          concerns: null
        }
      },
      {
        id: 2,
        date: "2025-01-23",
        analysis: {
          mood: "anxious",
          engagement: "moderate",
          patterns: ["isolation", "dark colors"],
          concerns: "potential school anxiety"
        }
      }
    ]
  };

  const emotionTrends = [
    { day: "Mon", score: 85 },
    { day: "Tue", score: 82 },
    { day: "Wed", score: 75 },
    { day: "Thu", score: 65 },
    { day: "Fri", score: 70 }
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Warning Banner */}
      {showAlert && (
        <div className="bg-orange-100 border-l-4 border-orange-500 p-4 mb-6">
          <div className="flex items-center">
            <AlertTriangle className="w-6 h-6 text-orange-500 mr-4" />
            <div>
              <p className="font-bold text-orange-800">Important Privacy Notice</p>
              <p className="text-orange-700">
                AI analysis is for guidance only. Always consult professionals for concerns. 
                Data is encrypted and analyzed locally.
              </p>
            </div>
            <button 
              className="ml-auto text-orange-500"
              onClick={() => setShowAlert(false)}
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Parent Dashboard</h1>
        <div className="flex gap-4">
          <select 
            className="p-2 rounded-lg border"
            value={selectedTimeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            <option value="week">Past Week</option>
            <option value="month">Past Month</option>
            <option value="year">Past Year</option>
          </select>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="col-span-2 bg-white rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Recent Drawings & Analysis</h2>
          <div className="space-y-4">
            {mockChildData.recentDrawings.map(drawing => (
              <div key={drawing.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-2 text-gray-500" />
                    <span className="text-sm text-gray-600">{drawing.date}</span>
                  </div>
                  {drawing.analysis.concerns && (
                    <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                      Needs Attention
                    </span>
                  )}
                </div>
                
                <div className="grid grid-cols-2 gap-4 mt-4">
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="flex items-center mb-2">
                      <Heart className="w-4 h-4 mr-2 text-pink-500" />
                      <span className="font-medium">Emotional State</span>
                    </div>
                    <p className="text-sm">{drawing.analysis.mood}</p>
                  </div>
                  
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="flex items-center mb-2">
                      <Brain className="w-4 h-4 mr-2 text-purple-500" />
                      <span className="font-medium">Engagement Level</span>
                    </div>
                    <p className="text-sm">{drawing.analysis.engagement}</p>
                  </div>
                </div>

                {drawing.analysis.concerns && (
                  <div className="mt-4 bg-yellow-50 p-4 rounded-lg">
                    <div className="flex items-start">
                      <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
                      <div>
                        <h4 className="font-medium text-yellow-800">Gentle Alert</h4>
                        <p className="text-sm text-yellow-700">{drawing.analysis.concerns}</p>
                        <div className="mt-2">
                          <button className="text-sm text-blue-600 hover:underline">
                            Suggested Support Strategies →
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-lg font-semibold mb-4">Emotional Wellbeing Trends</h3>
            <div className="space-y-4">
              {emotionTrends.map((day, i) => (
                <div key={i} className="flex items-center">
                  <span className="w-12 text-sm text-gray-600">{day.day}</span>
                  <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-blue-500 rounded-full"
                      style={{ width: `${day.score}%` }}
                    />
                  </div>
                  <span className="w-12 text-right text-sm text-gray-600">{day.score}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Professional Resources */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-lg font-semibold mb-4">Support Resources</h3>
            <div className="space-y-3">
              <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50">
                <div className="flex items-center">
                  <MessageCircle className="w-5 h-5 mr-3 text-blue-500" />
                  <span>Child Development Expert Chat</span>
                </div>
              </button>
              <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50">
                <div className="flex items-center">
                  <TrendingUp className="w-5 h-5 mr-3 text-green-500" />
                  <span>Progress Report</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParentDashboard;