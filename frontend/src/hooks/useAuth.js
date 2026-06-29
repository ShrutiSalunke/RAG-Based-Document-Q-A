// File location: frontend/src/hooks/useAuth.js
import { useCallback, useState } from "react";
import * as api from "../lib/api.js";
 
export function useAuth() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
 
  const login = useCallback(async (username, password) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.login(username, password);
      setIsLoggedIn(true);
      return true;
    } catch (err) {
      setError(err.message || "Login failed. Check your username and password.");
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);
 
  const logout = useCallback(() => {
    api.clearTokens();
    setIsLoggedIn(false);
  }, []);
 
  return { isLoggedIn, isLoading, error, login, logout };
}
 
