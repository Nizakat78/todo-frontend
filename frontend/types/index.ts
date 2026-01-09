// User interface based on the data model
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Task interface based on the data model
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  userId: string;
}

// Authentication state interface
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// Task state interface
export interface TaskState {
  tasks: Task[];
  currentTask: Task | null;
  isLoading: boolean;
  error: string | null;
  filters: {
    completed: 'all' | 'completed' | 'active';
    sortBy: 'created' | 'updated' | 'title';
  };
}

// API response interfaces
export interface LoginResponse {
  user: User;
  token: string;
  refreshToken?: string;
}

export interface LoginErrorResponse {
  error: string;
  message: string;
}

export interface GetTasksResponse {
  tasks: Task[];
  totalCount: number;
}

export interface GetTaskResponse {
  task: Task;
}

export interface TaskModificationResponse {
  task: Task;
  message: string;
}

export interface TaskErrorResponse {
  error: string;
  message: string;
}