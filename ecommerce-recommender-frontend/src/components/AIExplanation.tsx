'use client';

import React from 'react';

interface AIExplanationProps {
  explanation: string;
  userName: string;
}

export default function AIExplanation({ explanation, userName }: AIExplanationProps) {
  return (
    <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg shadow-md p-6 border border-purple-100">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
          <svg
            className="w-6 h-6 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-bold text-gray-900">AI Recommendation Insight</h3>
          <p className="text-sm text-gray-600">Personalized for {userName}</p>
        </div>
      </div>

      {/* Explanation Text */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <p className="text-gray-800 leading-relaxed">{explanation}</p>
      </div>

      {/* Footer */}
      <div className="mt-4 flex items-center gap-2 text-xs text-gray-500">
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 10V3L4 14h7v7l9-11h-7z"
          />
        </svg>
        <span>Powered by OpenAI GPT-3.5</span>
      </div>
    </div>
  );
}
