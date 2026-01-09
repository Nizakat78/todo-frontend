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
    const { user, token } = response.data;

    // Store in localStorage for the session
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));

    return { user, token };
  },

  signup: async (email: string, password: string, name?: string): Promise<LoginResponse> => {
    // Call the backend auth endpoint to register user and get JWT token
    const response = await apiClient.post('/auth/signup', { email, password, name });
    const { user, token } = response.data;

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

// Task API calls
const tasks = {
  getAll: async (userId: string): Promise<GetTasksResponse> => {
    const response = await apiClient.get(`/${userId}/tasks`);
    return response.data;
  },

  getById: async (userId: string, taskId: string): Promise<GetTaskResponse> => {
    const response = await apiClient.get(`/${userId}/tasks/${taskId}`);
    return response.data;
  },

  create: async (userId: string, taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'userId'>): Promise<TaskModificationResponse> => {
    const response = await apiClient.post(`/${userId}/tasks`, taskData);
    return response.data;
  },

  update: async (userId: string, taskId: string, taskData: Partial<Task>): Promise<TaskModificationResponse> => {
    const response = await apiClient.put(`/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  delete: async (userId: string, taskId: string): Promise<{ message: string }> => {
    const response = await apiClient.delete(`/${userId}/tasks/${taskId}`);
    return response.data;
  },

  updateCompletion: async (userId: string, taskId: string, completed: boolean): Promise<TaskModificationResponse> => {
    const response = await apiClient.patch(`/${userId}/tasks/${taskId}/complete`, { completed });
    return response.data;
  },
};

export { apiClient, auth, tasks };

// Export as default object for easier use
const api = {
  auth,
  tasks,
};

export default api;