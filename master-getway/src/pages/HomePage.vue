<template>
    <!-- Le pasamos la prop evaluando si activeRole tiene valor -->
    <Header :show-logout="!!activeRole" />
    <Navbar v-if="activeRole" :menu-items="useMenu().menu" />
    <MsjToast/>
    <div class="p-2 flex flex-col items-center w-full">
        
        <!-- CASO 1: Si AÚN NO selecciona un rol -->
        <template v-if="!activeRole">
            <div class="text-center mb-4">
                <h1 class="text-4xl font-bold text-[var(--surface-900)]">Bienvenido al Sistema Master Gateway</h1>
                <p class="italic text-[var(--surface-600)]">Selecciona un rol a continuación para continuar</p>
            </div>

            <div class="w-full flex justify-center mt-4">
                <SelectRolePage @select-role="handleRoleSelection" />
            </div>
        </template>

        <!-- CASO 2: Si YA seleccionó un rol -->
        <template v-else>
            <div class="w-full flex p-0 m-0 justify-between items-center">
                <div>
                    <Button 
                        @click="handleRoleChange"
                        severity="contrast"
                        label="Cambiar de Rol" 
                        icon="pi pi-arrow-left" 
                    />
                </div>
                <div>
                    <p class="flex items-center gap-1.5 m-0 font-bold text-[var(--surface-900)]">
                        <i :class="['pi', activeRole?.icon || 'pi-user']" class="text-lg"></i>
                        <span class="[overflow-wrap:anywhere] [word-break:break-word]">{{ activeRole?.name?.toUpperCase() }}</span>
                    </p>  
                </div>
            </div>
        </template>

        <div v-if="isLoading" class="fixed inset-0 w-full h-full bg-black/50 flex items-center justify-center z-[9999]">
            <ProgressSpinner 
                style="width: 40%; height: 40%;" 
                strokeWidth="8" 
                fill="transparent"
                animationDuration=".5s" 
                aria-label="Custom ProgressSpinner" 
            />
        </div>

    </div>

    <div v-if="activeRole">
        <router-view />
    </div>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import SelectRolePage from '@/pages/SelectRolePage.vue';
import ProgressSpinner from 'primevue/progressspinner';
import Header from '@/components/general/Header.vue';
import Navbar from '@/components/general/Navbar.vue';
import MsjToast from '@/components/general/MsjToast.vue';
import Button from 'primevue/button';
import { useAuth } from '@/helpers/useAuth.js';
import { useMenu } from '@/helpers/useMenu.js';

const router = useRouter();
const activeRole = ref(JSON.parse(localStorage.getItem('activeRole')) || null);
const isLoading = ref(false);

const handleRoleSelection = async (role) => {
    isLoading.value = true;
    try {
        await useAuth().selectRole(role.id);
        await useMenu().fetchMenu();
        activeRole.value = role;
        localStorage.setItem('activeRole', JSON.stringify(role));
    } catch (error) {
        console.error("Error al seleccionar rol", error);
    } finally {
        isLoading.value = false;
    }
};

const handleRoleChange = () => {
    activeRole.value = null;
    localStorage.removeItem('activeRole');
    // Redirige a la ruta principal o raíz para limpiar la vista anterior del router-view
    router.push('/'); 
};
</script>