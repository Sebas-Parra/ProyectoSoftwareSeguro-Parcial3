import { createRouter, createWebHistory } from 'vue-router';

// Lazy load pages
const LoginPage = () => import('@/pages/LoginPage.vue');

const routes = [
    //rutas
    {
      path: "/",
      redirect: "/login"
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'notfound',
        redirect: '/login'
    },
    {
        path: '/login', 
        name: 'login',
        component: LoginPage,
        meta: { requiresGuest: true }
    },
    {
        path: '/home',
        name: 'home',
        component: () => import('@/pages/HomePage.vue'),
        meta: { requiresAuth: true }
        // Las rutas hijas (admin/menus, admin/roles, sales, etc.) NO se
        // declaran aqui: se registran dinamicamente en tiempo de ejecucion
        // a partir del arbol de menu que devuelve el backend segun el rol
        // seleccionado. Ver src/router/viewRegistry.js y
        // src/helpers/useMenu.js (registerRoutesFromMenu).
    },

];

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth'
            }
        }
        return { top: 0 }
    }
});

// Guard global para proteger rutas con soporte de storage
router.beforeEach((to, from, next) => {
    // Sincroniza con el nombre de token que usas en authService / useAuth
    const tempToken = localStorage.getItem('tempToken') || localStorage.getItem('accessToken');
    const user = localStorage.getItem('user');
    const isAuthenticated = !!tempToken && !!user;

    // Si la ruta requiere autenticación y no está autenticado
    if (to.meta.requiresAuth) {
        if (!isAuthenticated) {
            localStorage.removeItem('tempToken');
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');
            localStorage.removeItem('activeRole');
            return next('/login');
        }
        return next();
    }
    
    // Si la ruta es solo para invitados (como el login) y ya está autenticado
    if (to.meta.requiresGuest) {
        if (isAuthenticated) {
            return next('/home');
        }
        return next();
    }
    
    next();
});

export default router;