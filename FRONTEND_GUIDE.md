# 🎨 Frontend Development Guide

Build a beautiful React + Tailwind CSS dashboard for your E-Commerce Recommender System.

---

## 📋 Table of Contents

1. Quick Setup (Next.js + Tailwind)
2. React Components
3. Full Dashboard Example
4. Styling Guide
5. API Integration
6. State Management

---

## 1. 🚀 Quick Setup

### **Option A: Next.js (Recommended)**

```bash
# Create Next.js app with Tailwind
npx create-next-app@latest ecommerce-recommender-frontend

# During setup, select:
# ✅ TypeScript? → Yes
# ✅ ESLint? → Yes
# ✅ Tailwind CSS? → Yes
# ✅ App Router? → Yes

cd ecommerce-recommender-frontend
npm install axios
npm run dev
```

Visit: http://localhost:3000

---

### **Option B: React + Vite (Faster)**

```bash
npm create vite@latest ecommerce-recommender-frontend -- --template react
cd ecommerce-recommender-frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install axios
npm run dev
```

---

## 2. 🧩 React Components

### **Component 1: User Selector**

Create: `src/components/UserSelector.jsx`

```jsx
import React from 'react';

const users = [
  { id: 1, name: 'Alice Johnson', emoji: '🎧', interest: 'Audio Enthusiast' },
  { id: 2, name: 'Bob Smith', emoji: '⌨️', interest: 'Computer Accessories' },
  { id: 3, name: 'Charlie Brown', emoji: '🏠', interest: 'Home Office' },
  { id: 4, name: 'Diana Prince', emoji: '📱', interest: 'Mobile Accessories' }
];

export default function UserSelector({ selectedUser, onSelectUser }) {
  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Select User</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {users.map(user => (
          <button
            key={user.id}
            onClick={() => onSelectUser(user.id)}
            className={`p-6 rounded-lg border-2 transition-all hover:shadow-lg ${
              selectedUser === user.id
                ? 'border-blue-500 bg-blue-50 shadow-md'
                : 'border-gray-200 bg-white hover:border-blue-300'
            }`}
          >
            <div className="text-4xl mb-2">{user.emoji}</div>
            <div className="font-semibold text-gray-800">{user.name}</div>
            <div className="text-sm text-gray-500">{user.interest}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

---

### **Component 2: Product Card**

Create: `src/components/ProductCard.jsx`

```jsx
import React from 'react';

export default function ProductCard({ product }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
      {/* Product Header */}
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-800 flex-1">
          {product.name}
        </h3>
        <span className="text-xl font-bold text-blue-600">
          ${product.price}
        </span>
      </div>

      {/* Category Badge */}
      <div className="mb-3">
        <span className="inline-block px-3 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800">
          {product.category}
        </span>
      </div>

      {/* Description */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {product.description}
      </p>

      {/* Tags */}
      <div className="flex flex-wrap gap-1 mb-4">
        {product.tags?.split(',').slice(0, 3).map((tag, idx) => (
          <span
            key={idx}
            className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded"
          >
            {tag.trim()}
          </span>
        ))}
      </div>

      {/* Recommendation Score */}
      {product.recommendation_score && (
        <div className="pt-3 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">Match Score</span>
            <div className="flex items-center">
              <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                  style={{ width: `${Math.min(product.recommendation_score * 5, 100)}%` }}
                />
              </div>
              <span className="ml-2 text-xs font-semibold text-gray-700">
                {product.recommendation_score.toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Action Button */}
      <button className="w-full mt-4 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
        View Details
      </button>
    </div>
  );
}
```

---

### **Component 3: AI Explanation Card**

Create: `src/components/AIExplanation.jsx`

```jsx
import React from 'react';

export default function AIExplanation({ explanation, userName, loading }) {
  if (loading) {
    return (
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-8 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-full"></div>
      </div>
    );
  }

  if (!explanation) return null;

  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-8 border border-blue-100">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
        </div>
        <div className="ml-4 flex-1">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            🤖 AI Recommendation Insights
          </h3>
          <p className="text-gray-700 leading-relaxed">
            {explanation}
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

### **Component 4: Loading Skeleton**

Create: `src/components/LoadingSkeleton.jsx`

```jsx
import React from 'react';

export default function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3, 4, 5, 6].map(i => (
        <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6 mb-4"></div>
          <div className="flex gap-2 mb-4">
            <div className="h-6 bg-gray-200 rounded w-16"></div>
            <div className="h-6 bg-gray-200 rounded w-16"></div>
            <div className="h-6 bg-gray-200 rounded w-16"></div>
          </div>
          <div className="h-10 bg-gray-200 rounded"></div>
        </div>
      ))}
    </div>
  );
}
```

---

## 3. 📱 Full Dashboard Example

Create: `src/app/page.jsx` (Next.js) or `src/App.jsx` (React)

```jsx
'use client'; // Remove this line if using React (not Next.js)

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserSelector from '@/components/UserSelector';
import ProductCard from '@/components/ProductCard';
import AIExplanation from '@/components/AIExplanation';
import LoadingSkeleton from '@/components/LoadingSkeleton';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function Dashboard() {
  const [selectedUser, setSelectedUser] = useState(1);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch recommendations when user changes
  useEffect(() => {
    fetchRecommendations(selectedUser);
  }, [selectedUser]);

  const fetchRecommendations = async (userId) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${API_BASE_URL}/recommend/${userId}?top_n=6`);
      setRecommendations(response.data);
    } catch (err) {
      setError('Failed to load recommendations. Make sure the backend is running!');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🛍️ E-Commerce Recommender
              </h1>
              <p className="text-gray-600 mt-1">
                AI-powered personalized product recommendations
              </p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => fetchRecommendations(selectedUser)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                🔄 Refresh
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Selector */}
        <UserSelector 
          selectedUser={selectedUser} 
          onSelectUser={setSelectedUser}
        />

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* AI Explanation */}
        {recommendations && !loading && (
          <>
            <AIExplanation 
              explanation={recommendations.llm_explanation}
              userName={recommendations.user_name}
              loading={loading}
            />

            {/* User Behavior Summary */}
            <div className="bg-white rounded-lg p-6 mb-8 border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                📊 User Activity Summary
              </h3>
              <p className="text-gray-600 text-sm whitespace-pre-line">
                {recommendations.user_behavior_summary}
              </p>
            </div>
          </>
        )}

        {/* Recommendations Header */}
        {recommendations && !loading && (
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-800">
              Recommended Products
            </h2>
            <p className="text-gray-600 mt-1">
              {recommendations.recommended_products.length} personalized recommendations for {recommendations.user_name}
            </p>
          </div>
        )}

        {/* Products Grid */}
        {loading ? (
          <LoadingSkeleton />
        ) : recommendations?.recommended_products ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.recommended_products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : null}

        {/* No Recommendations */}
        {!loading && recommendations?.recommended_products?.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🤷‍♂️</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              No recommendations available
            </h3>
            <p className="text-gray-600">
              Try selecting a different user or add more products to the database.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            Built with FastAPI + React + Tailwind CSS | Powered by OpenAI GPT
          </p>
        </div>
      </footer>
    </div>
  );
}
```

---

## 4. 🎨 Tailwind Configuration

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      animation: {
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/line-clamp'),
  ],
}
```

Update `src/app/globals.css` or `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    @apply antialiased;
  }
}

@layer utilities {
  .line-clamp-2 {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
  }
}
```

---

## 5. 🔌 API Service Setup

Create: `src/services/api.js`

```javascript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Methods
export const recommendationService = {
  // Get recommendations for a user
  getRecommendations: async (userId, topN = 6) => {
    const response = await api.get(`/recommend/${userId}`, {
      params: { top_n: topN }
    });
    return response.data;
  },

  // Get all users
  getAllUsers: async () => {
    const response = await api.get('/users');
    return response.data;
  },

  // Get all products
  getAllProducts: async (category = null) => {
    const response = await api.get('/products', {
      params: category ? { category } : {}
    });
    return response.data;
  },

  // Get product details
  getProduct: async (productId) => {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },

  // Get categories
  getCategories: async () => {
    const response = await api.get('/categories');
    return response.data;
  },

  // Add user interaction (view, click, purchase)
  addInteraction: async (userId, productId, actionType) => {
    const response = await api.post('/interactions', {
      user_id: userId,
      product_id: productId,
      action_type: actionType
    });
    return response.data;
  }
};

export default api;
```

---

## 6. 📦 Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

For production:

```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

---

## 7. 🚀 Running Both Frontend & Backend

### **Terminal 1: Backend**
```bash
cd backend
python -m uvicorn main:app --reload
```

### **Terminal 2: Frontend**
```bash
cd ecommerce-recommender-frontend
npm run dev
```

Visit: **http://localhost:3000**

---

## 8. 📱 Responsive Design Features

The dashboard includes:

- ✅ Mobile-first design
- ✅ Responsive grid layouts
- ✅ Touch-friendly buttons
- ✅ Smooth animations
- ✅ Loading states
- ✅ Error handling
- ✅ Accessibility features

---

## 9. 🎯 Next Steps

1. **Add Product Details Modal** - Click to see more info
2. **Shopping Cart** - Let users add items
3. **User Authentication** - Login system
4. **Search & Filters** - Find products easily
5. **Real-time Updates** - WebSocket integration
6. **Dark Mode** - Toggle theme

---

## 📦 Complete Package.json

```json
{
  "name": "ecommerce-recommender-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "axios": "^1.6.2",
    "next": "14.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@tailwindcss/line-clamp": "^0.4.4",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.54.0",
    "eslint-config-next": "14.0.3",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5"
  }
}
```

---

**🎉 Your frontend is ready! Now you have a beautiful UI for your recommender system!**

Next: See `CUSTOMIZE_RECOMMENDATIONS.md` for algorithm tuning.
