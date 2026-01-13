/**
 * API service for communicating with the backend
 */
import axios from 'axios';

// CRITICAL FIX: Use port 8000 consistently
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 180000, // 3 minutes timeout (AI generation can take 30-60 seconds)
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - backend may be slow or not responding');
    } else if (error.message === 'Network Error') {
      console.error('Network error - backend may not be running');
      console.error('Make sure backend is running on', API_BASE_URL);
    } else {
      console.error('API Response Error:', error.response?.status, error.message);
    }
    return Promise.reject(error);
  }
);

// Test Cases API
export const testCasesAPI = {
  // Generate a new test case from a prompt
  generate: async (prompt) => {
    // Use longer timeout for test case generation (AI can take 60+ seconds)
    const response = await api.post('/api/test-cases/generate', { prompt }, {
      timeout: 180000 // 3 minutes
    });
    return response.data;
  },

  // Get all test cases
  getAll: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append('status_filter', filters.status);
    if (filters.search) params.append('search', filters.search);
    
    const queryString = params.toString();
    const url = queryString ? `/api/test-cases?${queryString}` : '/api/test-cases';
    const response = await api.get(url);
    return response.data;
  },

  // Get a single test case
  getById: async (id) => {
    const response = await api.get(`/api/test-cases/${id}`);
    return response.data;
  },

  // Update a test case
  update: async (id, data) => {
    const response = await api.put(`/api/test-cases/${id}`, data);
    return response.data;
  },

  // Approve a test case
  approve: async (id) => {
    const response = await api.post(`/api/test-cases/${id}/approve`);
    return response.data;
  },

  // Delete a test case
  delete: async (id) => {
    const response = await api.delete(`/api/test-cases/${id}`);
    return response.data;
  },

  // Export test case to Excel
  exportExcel: async (id) => {
    const response = await api.get(`/api/test-cases/${id}/export-excel`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `test_case_${id}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  // Generate Selenium script
  generateSelenium: async (id) => {
    const response = await api.get(`/api/test-cases/${id}/generate-selenium`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `test_${id}.py`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
};

// Test Steps API
export const testStepsAPI = {
  // Create a new test step
  create: async (testCaseId, stepData) => {
    const response = await api.post(`/api/test-cases/${testCaseId}/steps`, stepData);
    return response.data;
  },

  // Update a test step
  update: async (testCaseId, stepId, stepData) => {
    const response = await api.put(`/api/test-cases/${testCaseId}/steps/${stepId}`, stepData);
    return response.data;
  },

  // Delete a test step
  delete: async (testCaseId, stepId) => {
    const response = await api.delete(`/api/test-cases/${testCaseId}/steps/${stepId}`);
    return response.data;
  },
};

// Stats API
export const statsAPI = {
  // Get dashboard statistics
  get: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  },
};

export default api;

