import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

export const fetchProjects = () => api.get('/api/v1/projects');
export const fetchProducts = () => api.get('/api/v1/products');
// Add more endpoints as needed

export default api;
