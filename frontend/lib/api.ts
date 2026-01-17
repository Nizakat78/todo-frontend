import axios from 'axios';
import { User, Task, LoginResponse, GetTasksResponse, GetTaskResponse, TaskModificationResponse } from '../types';

// Create an axios instance
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/api` : 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth data if token is invalid/expired
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

// Authentication API calls
const auth = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    // Call the backend auth endpoint to get JWT token
    const response = await apiClient.post('/auth/login', { email, password });
    // Backend returns { success, data: { id, email, name, ... }, token }
    const { data: userData, token } = response.data;

    // Map the user data to expected format
    const user: User = {
      id: userData.id,
      email: userData.email,
      name: userData.name,
      createdAt: userData.created_at,
      updatedAt: userData.updated_at,
    };

    // Store in localStorage for the session
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));

    return { user, token };
  },

  signup: async (email: string, password: string, name?: string): Promise<LoginResponse> => {
    // Call the backend auth endpoint to register user and get JWT token
    const response = await apiClient.post('/auth/signup', { email, password, name });
    // Backend returns { success, data: { id, email, name, ... }, token }
    const { data: userData, token } = response.data;

    // Map the user data to expected format
    const user: User = {
      id: userData.id,
      email: userData.email,
      name: userData.name,
      createdAt: userData.created_at,
      updatedAt: userData.updated_at,
    };

    // Store in localStorage for the session
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));

    return { user, token };
  },

  logout: async (): Promise<{ message: string }> => {
    // Call the backend logout endpoint to invalidate the token
    const response = await apiClient.post('/auth/logout');

    // Remove stored tokens
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    return response.data;
  },
};

// Helper function to map backend task to frontend Task type
const mapTask = (backendTask: any): Task => ({
  id: backendTask.id,
  title: backendTask.title,
  description: backendTask.description,
  completed: backendTask.completed,
  createdAt: backendTask.created_at,
  updatedAt: backendTask.updated_at,
  userId: backendTask.user_id,
});

// Task API calls
const tasks = {
  getAll: async (userId: string): Promise<GetTasksResponse> => {
    const response = await apiClient.get(`/${userId}/tasks`);
    // Backend returns { success, data: [tasks], meta: { total, limit, offset }, timestamp }
    const { data: tasksData, meta } = response.data;
    return {
      tasks: tasksData.map(mapTask),
      totalCount: meta?.total || tasksData.length,
    };
  },

  getById: async (userId: string, taskId: string): Promise<GetTaskResponse> => {
    const response = await apiClient.get(`/${userId}/tasks/${taskId}`);
    // Backend returns { success, data: task, timestamp }
    const { data: taskData } = response.data;
    return {
      task: mapTask(taskData),
    };
  },

  create: async (userId: string, taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'userId'>): Promise<TaskModificationResponse> => {
    const response = await apiClient.post(`/${userId}/tasks`, taskData);
    // Backend returns { success, data: task, timestamp }
    const { data: createdTask } = response.data;
    return {
      task: mapTask(createdTask),
      message: 'Task created successfully',
    };
  },

  update: async (userId: string, taskId: string, taskData: Partial<Task>): Promise<TaskModificationResponse> => {
    const response = await apiClient.put(`/${userId}/tasks/${taskId}`, taskData);
    // Backend returns { success, data: task, timestamp }
    const { data: updatedTask } = response.data;
    return {
      task: mapTask(updatedTask),
      message: 'Task updated successfully',
    };
  },

  delete: async (userId: string, taskId: string): Promise<{ message: string }> => {
    await apiClient.delete(`/${userId}/tasks/${taskId}`);
    // Backend returns 204 No Content
    return { message: 'Task deleted successfully' };
  },

  updateCompletion: async (userId: string, taskId: string, completed: boolean): Promise<TaskModificationResponse> => {
    const response = await apiClient.patch(`/${userId}/tasks/${taskId}/complete`, { completed });
    // Backend returns { success, data: task, timestamp }
    const { data: updatedTask } = response.data;
    return {
      task: mapTask(updatedTask),
      message: 'Task completion updated successfully',
    };
  },
};

export { apiClient, auth, tasks };

// Export as default object for easier use
const api = {
  auth,
  tasks,
};

export default api;