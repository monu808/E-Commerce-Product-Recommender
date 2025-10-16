'use client';

import { useState, useEffect } from 'react';
import UserSelector from '@/components/UserSelector';
import ProductCard from '@/components/ProductCard';
import AIExplanation from '@/components/AIExplanation';
import LoadingSkeleton from '@/components/LoadingSkeleton';
import { api, RecommendationResponse } from '@/services/api';

export default function Home() {
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (selectedUserId) {
      loadRecommendations(selectedUserId);
    }
  }, [selectedUserId]);

  const loadRecommendations = async (userId: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getRecommendations(userId);
      setRecommendations(data);
    } catch (err) {
      setError('Failed to load recommendations. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                E-commerce Product Recommender
              </h1>
              <p className="text-gray-600 text-sm mt-1">
                AI-powered personalized product recommendations
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Selector */}
        <div className="mb-8">
          <UserSelector
            selectedUserId={selectedUserId}
            onSelectUser={setSelectedUserId}
          />
        </div>

        {/* Loading State */}
        {loading && <LoadingSkeleton />}

        {/* Error State */}
        {error && !loading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <div className="flex items-center gap-3">
              <svg
                className="w-6 h-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <div>
                <p className="text-red-800 font-medium">{error}</p>
                <button
                  onClick={() => selectedUserId && loadRecommendations(selectedUserId)}
                  className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
                >
                  Try again
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Recommendations */}
        {recommendations && !loading && !error && (
          <div className="space-y-8">
            {/* AI Explanation */}
            <AIExplanation
              explanation={recommendations.llm_explanation}
              userName={recommendations.user_name}
            />

            {/* Products Grid */}
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  Recommended for {recommendations.user_name}
                </h2>
                <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  {recommendations.recommended_products.length} products
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.recommended_products.map((product, index) => (
                  <ProductCard key={product.id} product={product} index={index} />
                ))}
              </div>
            </div>

            {/* Timestamp */}
            <div className="text-center text-sm text-gray-500">
              Generated at {new Date(recommendations.timestamp || new Date()).toLocaleString()}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!selectedUserId && !loading && (
          <div className="text-center py-16">
            <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-12 h-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Select a user to get started
            </h3>
            <p className="text-gray-500">
              Choose a user from the dropdown above to see personalized recommendations
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-600 text-sm">
              © 2025 E-commerce Recommender. Powered by FastAPI + OpenAI.
            </p>
            <div className="flex items-center gap-6 text-sm text-gray-500">
              <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">
                API Docs
              </a>
              <a href="https://github.com/monu808/E-Commerce-Product-Recommender" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

