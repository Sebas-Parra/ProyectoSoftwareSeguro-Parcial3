// services/saleService.js
import { apiClientSale } from './api.js';

export const saleService = {
  async getSales(page = 1, limit = 5) {
    const response = await apiClientSale.get(`/sale?page=${page}&limit=${limit}`,{}, { useAccessToken: true });
    return response.data; // <-- Retornamos .data para acceder al JSON del backend
  },

  async createSale(payload) {
    const response = await apiClientSale.post('/sale', payload, { useAccessToken: true });
    return response.data;
  },

  async updateSale(id, payload) {
    const response = await apiClientSale.put(`/sale/${id}`, payload, { useAccessToken: true });
    return response.data;
  },

  async deleteSale(id) {
    const response = await apiClientSale.delete(`/sale/${id}`,{}, { useAccessToken: true });
    return response.data;
  }
};