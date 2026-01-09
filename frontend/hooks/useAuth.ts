"use client"
import { useAuth as useAuthContext } from '../contexts/AuthContext';

// This hook provides a cleaner way to access the auth context
// It's a simple wrapper around the context hook
export const useAuth = () => {
  return useAuthContext();
};