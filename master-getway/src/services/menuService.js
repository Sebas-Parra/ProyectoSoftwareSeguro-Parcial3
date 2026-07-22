// services/menuService.js
import { apiClientAuth } from './api.js';

export const menuService = {

    getMenusTree() {
        return apiClientAuth.get('/menus/tree', {}, { useAccessToken: true });
    },

    /**
     * Obtener todos los menús
     */
    getMenus() {
        return apiClientAuth.get('/menus', {}, { useAccessToken: true });
    },

    /**
     * Crear un menú
     */
    createMenu(menuData) {
        return apiClientAuth.post('/menus', menuData, { useAccessToken: true });
    },

    /**
     * Actualizar menú
     */
    updateMenu(menuId, menuData) {
        return apiClientAuth.put(`/menus/${menuId}`, menuData, { useAccessToken: true });
    },

    /**
     * Eliminar menú
     */
    deleteMenu(menuId) {
        return apiClientAuth.delete(`/menus/${menuId}`, { useAccessToken: true });
    },

    /**
     * Asignar menú a un rol
     * @param {number} menuId 
     * @param {number} roleId 
     */
    assignMenuToRole(menuId, roleId) {
        return apiClientAuth.post(`/roles/${menuId}/menus/${roleId}`, {}, { useAccessToken: true });
    }
};