import React, { createContext, useState, useEffect } from "react";
import api from "../utils/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(
    localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null
  );
  const [user, setUser] = useState(authTokens ? JSON.parse(atob(authTokens.access.split(".")[1])) : null);

  const login = async (username, password) => {
    const response = await api.post("accounts/login/", { username, password });
    const { access, refresh } = response.data;
    const tokens = { access, refresh };
    setAuthTokens(tokens);
    setUser(JSON.parse(atob(access.split(".")[1])));
    localStorage.setItem("authTokens", JSON.stringify(tokens)); // Persist tokens in localStorage
  };

  const logout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens"); // Clear tokens from localStorage
  };

  useEffect(() => {
    if (authTokens) {
      setUser(JSON.parse(atob(authTokens.access.split(".")[1])));
    }
  }, [authTokens]);

  return (
    <AuthContext.Provider value={{ user, authTokens, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
