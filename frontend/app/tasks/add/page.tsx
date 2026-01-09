'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Task } from '../../../types';
import { tasks as taskApi } from '../../../lib/api';
import TaskForm from '../../../components/TaskForm';
import Card from '../../../components/ui/Card';
import Button from '../../../components/ui/Button';
import { useAuth } from '../../../hooks/useAuth';

const AddTaskPage = () => {
  const router = useRouter();
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
        <div className="max-w-md w-full text-center">
          <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center mb-6">
            <svg className="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h2>
          <p className="text-gray-600 mb-6">Please sign in to create tasks.</p>
          <Link href="/login">
            <Button variant="primary">Sign In</Button>
          </Link>
        </div>
      </div>
    );
  }

  const handleSubmit = async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'userId'>) => {
    try {
      if (user?.id) {
        await taskApi.create(user.id, taskData);
        // Redirect to dashboard after successful creation
        router.push('/dashboard');
        router.refresh(); // Refresh to update the UI
      }
    } catch (error) {
      console.error('Error creating task:', error);
      // In a real app, you might want to show an error message to the user
    }
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Create New Task</h1>
            <p className="text-gray-600 mt-2">Add a new task to your list</p>
          </div>
          <Link href="/dashboard">
            <Button variant="secondary" className="flex items-center">
              <svg className="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Dashboard
            </Button>
          </Link>
        </div>

        <Card className="shadow-xl">
          <Card.Content>
            <TaskForm
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              submitButtonText="Create Task"
            />
          </Card.Content>
        </Card>
      </div>
    </div>
  );
};

export default AddTaskPage;