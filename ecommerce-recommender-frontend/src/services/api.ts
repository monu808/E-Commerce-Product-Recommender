import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface User {
  id: number;
  name: string;
}

export interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  description: string;
  tags: string[] | string; // Can be array or comma-separated string
}

export interface RecommendationResponse {
  user_id: number;
  user_name: string;
  recommended_products: Product[];
  llm_explanation: string;
  user_behavior_summary: string;
  timestamp?: string;
}

export const api = {
  // Get all users
  getUsers: async (): Promise<User[]> => {
    const response = await apiClient.get('/users');
    // Backend returns { count: number, users: User[] }
    return response.data.users || response.data;
  },

  // Get recommendations for a user
  getRecommendations: async (userId: number): Promise<RecommendationResponse> => {
    const response = await apiClient.get(`/recommend/${userId}`);
    // Add timestamp if not present
    return {
      ...response.data,
      timestamp: response.data.timestamp || new Date().toISOString()
    };
  },

  // Get all products
  getProducts: async (): Promise<Product[]> => {
    const response = await apiClient.get('/products');
    // Backend returns { count: number, products: Product[] }
    return response.data.products || response.data;
  },

  // Get all categories
  getCategories: async (): Promise<string[]> => {
    const response = await apiClient.get('/categories');
    // Backend returns { categories: string[] }
    return response.data.categories || response.data;
  },
};

export default api;
