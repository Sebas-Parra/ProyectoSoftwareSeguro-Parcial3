// services/roleService.js
import { apiClientAuth } from './api.js';

export const roleService = {
    /**
     * Obtener todos los roles
     */
    getRoles() {
        return apiClientAuth.get('/roles',{}, { useAccessToken: true });
    },

    /**
     * Crear un rol
     */
    createRole(roleData) {
        return apiClientAuth.post('/roles', roleData, { useAccessToken: true });
    },

    /**
     * Actualizar rol
     */
    updateRole(roleId, roleData) {
        return apiClientAuth.put(`/roles/${roleId}`, roleData, { useAccessToken: true });
    },

    /**
     * Eliminar rol
     */
    deleteRole(roleId) {
        return apiClientAuth.delete(`/roles/${roleId}`, { useAccessToken: true });
    },

    /**
     * Asignar rol a un usuario
     * @param {number} roleId 
     * @param {number} userId 
     */
    assignRoleToUser(roleId, userId) {
        return apiClientAuth.post(`/roles/${roleId}/user/${userId}`, {}, { useAccessToken: true });
    },

    /**
     * Desasignar rol de un usuario
     * @param {number} roleId 
     * @param {number} userId 
     */
    removeRoleFromUser(roleId, userId) {
        return apiClientAuth.delete(`/roles/${roleId}/user/${userId}`, { useAccessToken: true });
    }
};