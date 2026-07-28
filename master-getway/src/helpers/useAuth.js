import { ref, computed } from 'vue';
import authService from '@/services/authService.js';
import router from '@/router/router.js';
import { useMenu } from '@/helpers/useMenu.js';

const user = ref(null);

/**
 * Cargar usuario desde localStorage al iniciar la app
 */
function loadUserFromStorage() {
    const storedUser = localStorage.getItem('user');
    if (storedUser && storedUser !== "undefined" && storedUser !== "null") {
        try {
            user.value = JSON.parse(storedUser);
        } catch (e) {
            console.error("Error al parsear el usuario del localStorage", e);
            user.value = null;
        }
    }
}

loadUserFromStorage();

export function useAuth() {

    async function login(username, password) {
        try {
            const { data } = await authService.login({ username, password });
            
            authService.setTempToken(data.temp_token);
            
            const userData = {
                username: username,
                roles: data.roles || [] 
            };
            
            user.value = userData;
            localStorage.setItem('user', JSON.stringify(userData));
            
            return data;
        } catch (err) {
            // error.value = err.response?.data?.message || 'Error en el login';
            throw err.value;
        } 
    }

    async function selectRole(roleId) {

        try {

            const { data } = await authService.selectRole({ role_id: roleId });
            authService.setTokens(data.access_token, data.refresh_token);

            return data;
        } catch (err) {
            // error.value = err.response?.data?.message || 'Error al seleccionar el rol';
            throw err.value;
        } 
    }

    async function logout() {
        try {
            await authService.logout();
        } catch (error) {
            console.error("Error al cerrar sesión en el servidor", error);
        } finally {
            authService.clearTokens();
            user.value = null;
            localStorage.removeItem('user');
            localStorage.removeItem('activeRole');
            localStorage.removeItem('menu');

            const { menu, clearDynamicRoutes } = useMenu();
            clearDynamicRoutes();
            menu.value = [];

            router.push('/login');
        }
    }

    const isAuthenticated = computed(() => authService.isAuthenticated());

    return {
        // Estado
        user,
        
        // Métodos
        login,
        logout,
        loadUserFromStorage,
        selectRole,
        
        // Computados
        isAuthenticated
    };
}