'use client';

import React from 'react';
import { Product } from '@/services/api';

interface ProductCardProps {
  product: Product;
  index: number;
}

export default function ProductCard({ product, index }: ProductCardProps) {
  // Handle tags being either string or array
  const tags: string[] = Array.isArray(product.tags) 
    ? product.tags 
    : typeof product.tags === 'string' 
      ? product.tags.split(',').map((t: string) => t.trim()).filter((t: string) => t)
      : [];

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden">
      {/* Product Header */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4">
        <div className="flex items-center justify-between">
          <span className="inline-flex items-center justify-center w-8 h-8 bg-white rounded-full text-purple-600 font-bold text-sm">
            #{index + 1}
          </span>
          <span className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-white text-xs font-medium">
            {product.category}
          </span>
        </div>
      </div>

      {/* Product Content */}
      <div className="p-5">
        <h3 className="text-xl font-bold text-gray-900 mb-2">{product.name}</h3>
        
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">{product.description}</p>

        {/* Price */}
        <div className="mb-4">
          <span className="text-3xl font-bold text-green-600">${product.price}</span>
          <span className="text-gray-500 text-sm ml-1">.00</span>
        </div>

        {/* Tags */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {tags.map((tag: string, idx: number) => (
              <span
                key={idx}
                className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-medium"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Action Button */}
        <button className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105">
          View Details
        </button>
      </div>
    </div>
  );
}
