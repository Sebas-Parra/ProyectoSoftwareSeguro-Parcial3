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
        meta: { requiresAuth: true },
        children: [
            {
                path: 'admin/menus',
                name: 'admin-menus',
                component: () => import('@/pages/MenuPage.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'admin/roles',
                name: 'admin-roles',
                component: () => import('@/pages/RolePage.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'admin/users',
                name: 'admin-users',
                component: () => import('@/pages/UserPage.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'admin/modules',
                name: 'admin-modules',
                component: () => import('@/pages/ModulePage.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'sale',
                name: 'sale',
                component: () => import('@/pages/SalePage.vue'),
                meta: { requiresAuth: true }
            }
        ]
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