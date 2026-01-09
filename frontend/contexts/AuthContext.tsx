"use client"
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { User, AuthState } from '../types';
import { auth } from '../lib/api';

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuthStatus: () => void;
}

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'LOGIN_FAILURE'; payload: { error: string } }
  | { type: 'SIGNUP_START' }
  | { type: 'SIGNUP_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'SIGNUP_FAILURE'; payload: { error: string } }
  | { type: 'LOGOUT' }
  | { type: 'CHECK_AUTH_STATUS'; payload: { user: User | null; token: string | null } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'CLEAR_ERROR' };

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
    case 'SIGNUP_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
    case 'SIGNUP_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_FAILURE':
    case 'SIGNUP_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload.error,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      };
    case 'CHECK_AUTH_STATUS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: !!action.payload.token,
        isLoading: false,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const checkAuthStatus = () => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');

    if (token && user && user !== 'undefined') {
      try {
        const parsedUser = JSON.parse(user) as User;
        dispatch({
          type: 'CHECK_AUTH_STATUS',
          payload: { user: parsedUser, token },
        });
      } catch (error) {
        console.error('Error parsing user data:', error);
        dispatch({
          type: 'CHECK_AUTH_STATUS',
          payload: { user: null, token: null },
        });
      }
    } else {
      dispatch({
        type: 'CHECK_AUTH_STATUS',
        payload: { user: null, token: null },
      });
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await auth.login(email, password);
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: {
          user: response.user,
          token: response.token,
        },
      });
    } catch (error: any) {
      const errorMessage = error?.response?.data?.message || error.message || 'Login failed';
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: { error: errorMessage },
      });
      throw error;
    }
  };

  const signup = async (email: string, password: string, name?: string) => {
    dispatch({ type: 'SIGNUP_START' });
    try {
      const response = await auth.signup(email, password, name);
      dispatch({
        type: 'SIGNUP_SUCCESS',
        payload: {
          user: response.user,
          token: response.token,
        },
      });
    } catch (error: any) {
      const errorMessage = error?.response?.data?.message || error.message || 'Signup failed';
      dispatch({
        type: 'SIGNUP_FAILURE',
        payload: { error: errorMessage },
      });
      throw error;
    }
  };

  const logout = async () => {
    try {
      await auth.logout();
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      dispatch({ type: 'LOGOUT' });
    }
  };

  const value = {
    ...state,
    login,
    signup,
    logout,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};