"use client"
import React, { useState, useEffect } from 'react';
import { Task } from '../types';
import Input from './ui/Input';

interface FilterSortProps {
  tasks: Task[];
  onFilterAndSort: (filteredTasks: Task[]) => void;
}

const FilterSort: React.FC<FilterSortProps> = ({ tasks, onFilterAndSort }) => {
  const [filter, setFilter] = useState<'all' | 'completed' | 'active'>('all');
  const [sortBy, setSortBy] = useState<'created' | 'updated' | 'title'>('created');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    let filtered = [...tasks];

    // Apply filter
    if (filter === 'completed') {
      filtered = filtered.filter(task => task.completed);
    } else if (filter === 'active') {
      filtered = filtered.filter(task => !task.completed);
    }

    // Apply search
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(term) ||
        task.description.toLowerCase().includes(term)
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let comparison = 0;

      if (sortBy === 'title') {
        comparison = a.title.localeCompare(b.title);
      } else if (sortBy === 'updated') {
        comparison = new Date(a.updatedAt).getTime() - new Date(b.updatedAt).getTime();
      } else { // sortBy === 'created'
        comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
      }

      return sortOrder === 'asc' ? comparison : -comparison;
    });

    onFilterAndSort(filtered);
  }, [tasks, filter, sortBy, sortOrder, searchTerm, onFilterAndSort]);

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Filter</label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as 'all' | 'completed' | 'active')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="all">All Tasks</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'created' | 'updated' | 'title')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="created">Created Date</option>
            <option value="updated">Updated Date</option>
            <option value="title">Title</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Order</label>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>
        </div>

        <div>
          <Input
            label="Search"
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search tasks..."
          />
        </div>
      </div>
    </div>
  );
};

export default FilterSort;