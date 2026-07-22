import { apiClientAuth } from './api.js';

export const authService = {    

    /**
     * Login de usuario
     */
    login(credentials) {
        return apiClientAuth.post('/auth/login', credentials);
    },

    /**
     * Seleccionar rol de usuario
     */
    selectRole(credentials) {
        return apiClientAuth.post('/auth/select-role', credentials, { useTempToken: true });
    },

    /**
     * Refrescar access token
     */
    refreshToken(token) {
        return apiClientAuth.post('/auth/refresh-token', { token });
    },

    /**
     * Logout del usuario
     */
    logout() {
        return apiClientAuth.post('/auth/logout');
    },

    /**
     * Guardar token temporal en localStorage
     */
    setTempToken(temp_token) {
        localStorage.setItem('tempToken', temp_token);
    },

    /**
     * Guardar access token y refresh token en localStorage
     */
    setTokens(accessToken, refreshToken) {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
    },

    /**
     * Obtener el access token
     */
    getAccessToken() {
        return localStorage.getItem('accessToken');
    },

    /**
     * Obtener el refresh token
     */
    getRefreshToken() {
        return localStorage.getItem('refreshToken');
    },

    /**
     * Limpiar tokens
     */
    clearTokens() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('tempToken');
        localStorage.removeItem('roles');
    },

    /**
     * Verificar si existe token
     */
    isAuthenticated() {
        return !!localStorage.getItem('accessToken');
    }
};

export default authService;
