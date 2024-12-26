import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

api.interceptors.request.use((config) => {
  const authTokens = localStorage.getItem("authTokens");
  if (authTokens) {
    config.headers.Authorization = `Bearer ${JSON.parse(authTokens).access}`;
  }
  return config;
});

export const getTasks = async () => api.get("tasks/");
export const createTask = async (task) => api.post("tasks/", task);
export const updateTask = async (id, updatedTask) => api.put(`tasks/${id}/`, updatedTask);
export const deleteTask = async (id) => api.delete(`tasks/${id}/`);

export default api;