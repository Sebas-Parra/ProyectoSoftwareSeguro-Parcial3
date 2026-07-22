// services/userService.js
import { apiClientAuth } from './api.js';

export const userService = {
    /**
     * Obtener usuarios con paginación
     */
    getUsers(page = 1, limit = 10) {
        return apiClientAuth.get('/users', {
            params: { page, limit }
        }, { useAccessToken: true });
    },

    /**
     * Crear un usuario
     * @param {{ username: str, password: str }} userData 
     */
    createUser(userData) {
        return apiClientAuth.post('/users', userData, { useAccessToken: true });
    },

    /**
     * Actualizar usuario
     * @param {number} userId 
     * @param {{ username: str, password: str }} userData 
     */
    updateUser(userId, userData) {
        return apiClientAuth.put(`/users/${userId}`, userData, { useAccessToken: true });
    },

    /**
     * Eliminar usuario
     * @param {number} userId 
     */
    deleteUser(userId) {
        return apiClientAuth.delete(`/users/${userId}`, { useAccessToken: true });
    }
};