// services/moduleService.js
import { apiClientAuth } from './api.js';

export const moduleService = {
    /**
     * Obtener todos los módulos
     */
    getModules() {
        return apiClientAuth.get('/modules', {}, { useAccessToken: true });
    },

    /**
     * Crear un módulo
     */
    createModule(moduleData) {
        return apiClientAuth.post('/modules', moduleData, { useAccessToken: true });
    },

    /**
     * Actualizar módulo
     */
    updateModule(moduleId, moduleData) {
        return apiClientAuth.put(`/modules/${moduleId}`, moduleData, { useAccessToken: true });
    },

    /**
     * Eliminar módulo
     */
    deleteModule(moduleId) {
        return apiClientAuth.delete(`/modules/${moduleId}`, { useAccessToken: true });
    },

    /**
     * Asignar módulo a un rol
     * @param {number} moduleId 
     * @param {number} roleId 
     */
    assignModuleToRole(moduleId, roleId) {
        return apiClientAuth.post(`/roles/${moduleId}/modules/${roleId}`, {}, { useAccessToken: true });
    }
};