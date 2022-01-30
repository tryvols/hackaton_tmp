import axios from 'axios';

export const backend = axios.create({
  baseURL: `http://${window.location.hostname}:8000/api`,
  timeout: 3000
});

backend.interceptors.request.use((config) => {
  return config;
}, error => {
  return error;
});

export const setBackendToken = token => {
  if (!token) {
    return;
  }

  backend.defaults.headers.Authorization = `Bearer ${token}`;
};
