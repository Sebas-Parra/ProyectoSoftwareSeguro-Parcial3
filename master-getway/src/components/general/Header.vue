<template>
    <ConfirmDialog></ConfirmDialog>
    <div class="flex justify-between items-center w-full border-b border-black/30 pb-2">
        <div class="flex items-center gap-2">
            <div class="flex justify-center items-center ml-2">
                <img :src="LogoDark" alt="Logo" class="w-[100px] p-[10%] rounded-[20%]" />
            </div>
            <div>
                <h2 class="text-xl font-bold">Master Gateway</h2>
            </div>
        </div>
        <div v-if="showLogout" class="flex justify-center items-center gap-2 p-2">
            <Button icon="pi pi-sign-out" severity="danger" label="Cerrar Sesión" size="large" @click="handleLogout"
                title="Cerrar sesión" />
        </div>
    </div>
    <NavBar />
    <div v-if="isLoading" class="fixed inset-0 w-full h-full bg-black/50 flex items-center justify-center z-[9999]">
        <ProgressSpinner 
            style="width: 40%; height: 40%;" 
            strokeWidth="8" 
            fill="transparent"
            animationDuration=".5s" 
            aria-label="Custom ProgressSpinner" 
        />
    </div>
</template>

<script setup>

import LogoDark from '@/assets/LogoBi.png';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import ConfirmDialog from 'primevue/confirmdialog';
import { useAuth } from '@/helpers/useAuth.js';
import { useConfirm } from "primevue/useconfirm";
import { ref } from 'vue';

const { logout } = useAuth();
const confirm = useConfirm();
const isLoading = ref(false);

defineProps({
    showLogout: {
        type: Boolean,
        default: true
    }
});

const handleLogout = () => {
    confirm.require({
        message: "¿Seguro que desea cerrar sesión?",
        header: 'Cerrar Sesión',
        icon: 'pi pi-exclamation-circle',
        acceptProps: { label: 'Cerrar sesión', severity: 'danger' },
        rejectProps: { label: 'Cancelar', severity: 'secondary', outlined: true },
        accept: async () => {
            isLoading.value = true;
            await new Promise(resolve => setTimeout(resolve, 2000));
            logout();
            isLoading.value = false;
        }
    });
};

</script>