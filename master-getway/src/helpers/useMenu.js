import { ref, computed } from 'vue';
import { menuService } from '@/services/menuService.js';

const menu = ref([]);

/**
 * Cargar MENU desde localStorage al iniciar la app
 */
function loadMenuFromStorage() {
    const storedMenu = localStorage.getItem('menu');
    if (storedMenu && storedMenu !== "undefined" && storedMenu !== "null") {
        try {
            menu.value = JSON.parse(storedMenu);
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

        } catch (err) {
            console.error('Error al obtener el menú:', err);
        }

    }

    return {
        menu,
        fetchMenu
    };

}