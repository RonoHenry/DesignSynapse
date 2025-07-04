import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export const fetchProducts = async () => {
  const res = await axios.get(`${API_URL}/products`);
  return res.data;
};

export const fetchProjects = async () => {
  const res = await axios.get(`${API_URL}/projects`);
  return res.data;
};

export const fetchVendors = async () => {
  const res = await axios.get(`${API_URL}/vendors`);
  return res.data;
};
// Add more as needed
