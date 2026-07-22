<template>
    <div>
        <Menubar    
            :model="items"
            style="font-size: 1.1rem; background-color: #f6f6f6;" 
        >
            <template #start>
                <div style="padding: 10% 0% 10% 0%; display: flex; align-items: center; gap: 0.5rem;">
                    <Button icon="pi pi-user" severity="contrast" variant="text" rounded aria-label="User" />
                    <span style="color: #000; font-weight: 500; margin-right: 10%;">{{ user?.username || 'Usuario' }}</span>
                </div>
            </template>
            <template #separator> 
                |
            </template>
        </Menubar>
    </div>
</template>

<script setup>
import Menubar from 'primevue/menubar';
import router from '@/router/router';
import Button from 'primevue/button';
import { ref, onMounted, computed } from "vue";
import { useRoute } from 'vue-router';
import { useMenu } from '@/helpers/useMenu.js'; 
import { useAuth } from '@/helpers/useAuth.js';

const route = useRoute();
const userName = ref('');
const isDark = ref(false);

const { user } = useAuth();
// Usamos el composable para obtener el menú reactivo
const { menu } = useMenu();

// Detectar cuando PrimeVue cambia a modo oscuro
const checkDarkMode = () => {
    isDark.value = document.documentElement.classList.contains("my-app-dark");
};

onMounted(() => {
    checkDarkMode();

    const storedUser = localStorage.getItem('user');
    if (storedUser) {
        userName.value = storedUser.replace(/^"|"$/g, '').toUpperCase();
    }

    // Observar cambios en la clase del <html>
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"]
    });
});

/**
 * Función recursiva para transformar el JSON del backend/storage 
 * al formato compatible con PrimeVue (Menubar)
 */
const transformMenuData = (menuItems) => {
    if (!Array.isArray(menuItems)) return [];

    return menuItems.map(item => {
        const hasChildren = item.children && item.children.length > 0;
        
        let menuItem = {
            label: item.nombre,
            // Puedes asignar un icono por defecto o mapearlo según tus necesidades
            icon: item.icon || (hasChildren ? 'pi pi-folder' : 'pi pi-file'),
        };

        // Si tiene hijos, se procesan recursivamente
        if (hasChildren) {
            menuItem.items = transformMenuData(item.children);
        } else if (item.url) {
            // Si tiene URL y no es padre, maneja la navegación o apertura externa
            if (item.url.startsWith('http')) {
                menuItem.command = () => {
                    window.open(item.url, '_blank');
                };
            } else {
                menuItem.command = () => {
                    router.push(item.url);
                };
            }
            
            // Marcar clase activa si la ruta actual coincide con la URL del item
            const isActive = route.path === item.url || (item.url !== '/' && route.path.includes(item.url));
            menuItem.class = isActive ? 'active-item' : '';
        }

        return menuItem;
    });
};

// Computed que transforma automáticamente el menú cada vez que cambia en el storage/estado
const items = computed(() => {
    return transformMenuData(menu.value);
});
</script>

<style scoped>


</style>