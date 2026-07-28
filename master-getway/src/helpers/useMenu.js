import { ref, computed } from 'vue';
import { menuService } from '@/services/menuService.js';
import router from '@/router/router.js';
import viewRegistry from '@/router/viewRegistry.js';

const menu = ref([]);

// Nombres de las rutas dinamicas registradas actualmente, para poder
// quitarlas (router.removeRoute) antes de registrar las del siguiente rol.
let registeredRouteNames = [];

/**
 * A partir del arbol de menu devuelto por el backend, registra en el
 * Vue Router SOLO las rutas hoja (las que traen `url`) cuyo componente
 * exista en el viewRegistry. Nada de esto esta hardcodeado: si el backend
 * cambia el arbol (nuevo rol, nuevos permisos, nuevo item), las rutas
 * disponibles cambian con el, sin tocar el router.js.
 */
function registerRoutesFromMenu(menuTree) {
    clearDynamicRoutes();

    if (!Array.isArray(menuTree)) return;

    const walk = (items) => {
        for (const item of items) {
            if (Array.isArray(item.children) && item.children.length > 0) {
                walk(item.children);
                continue;
            }

            if (!item.url || item.url.startsWith('http')) continue;

            const relativePath = item.url.replace(/^\/home\//, '');
            const loadComponent = viewRegistry[relativePath];

            if (!loadComponent) {
                console.warn(`[menu] El backend devolvio la url "${item.url}" pero no hay vista registrada para ella en viewRegistry.js`);
                continue;
            }

            const routeName = `dynamic-${relativePath}`;
            router.addRoute('home', {
                path: relativePath,
                name: routeName,
                component: loadComponent,
                meta: { requiresAuth: true }
            });
            registeredRouteNames.push(routeName);
        }
    };

    walk(menuTree);
}

function clearDynamicRoutes() {
    for (const name of registeredRouteNames) {
        if (router.hasRoute(name)) {
            router.removeRoute(name);
        }
    }
    registeredRouteNames = [];
}

/**
 * Cargar MENU desde localStorage al iniciar la app
 */
function loadMenuFromStorage() {
    const storedMenu = localStorage.getItem('menu');
    if (storedMenu && storedMenu !== "undefined" && storedMenu !== "null") {
        try {
            menu.value = JSON.parse(storedMenu);
            registerRoutesFromMenu(menu.value);
        } catch (e) {
            console.error("Error al parsear el menú del localStorage", e);
            menu.value = null;
        }
    }
}

loadMenuFromStorage();

export function useMenu() {


    async function fetchMenu() {
        try {
            const { data } = await menuService.getMenusTree();
            menu.value = data;

            localStorage.setItem('menu', JSON.stringify(data));
            registerRoutesFromMenu(data);

        } catch (err) {
            console.error('Error al obtener el menú:', err);
        }

    }

    return {
        menu,
        fetchMenu,
        clearDynamicRoutes
    };

}

// Exportadas ademas a nivel de modulo (sin pasar por el composable) para
// poder probarlas de forma aislada.
export { registerRoutesFromMenu, clearDynamicRoutes };