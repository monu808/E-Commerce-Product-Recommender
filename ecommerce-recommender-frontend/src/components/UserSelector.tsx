'use client';

import React, { useEffect, useState } from 'react';
import { api, User } from '@/services/api';

interface UserSelectorProps {
  selectedUserId: number | null;
  onSelectUser: (userId: number) => void;
}

export default function UserSelector({ selectedUserId, onSelectUser }: UserSelectorProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getUsers();
      setUsers(data);
      
      // Auto-select first user if none selected
      if (data.length > 0 && !selectedUserId) {
        onSelectUser(data[0].id);
      }
    } catch (err) {
      setError('Failed to load users. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-600 font-medium mb-2">⚠️ Error</p>
        <p className="text-red-700 text-sm">{error}</p>
        <button
          onClick={loadUsers}
          className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <label htmlFor="user-select" className="block text-sm font-medium text-gray-700 mb-2">
        Select a User
      </label>
      <select
        id="user-select"
        value={selectedUserId || ''}
        onChange={(e) => onSelectUser(Number(e.target.value))}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
      >
        <option value="" disabled>
          Choose a user...
        </option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.name}
          </option>
        ))}
      </select>
      <p className="mt-2 text-xs text-gray-500">
        {users.length} user{users.length !== 1 ? 's' : ''} available
      </p>
    </div>
  );
}
