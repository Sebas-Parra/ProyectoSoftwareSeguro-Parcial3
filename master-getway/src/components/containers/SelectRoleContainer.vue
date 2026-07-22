<template>
    <div class="w-full max-w-[650px] bg-[var(--surface-section)] border border-[var(--surface-border)] rounded-2xl p-10 shadow-[0_10px_25px_rgba(0,0,0,0.05)]">
        <div class="text-center mb-6">
            <h1 class="text-[1.8rem] font-bold text-[var(--surface-900)] mt-0 mb-2">Selecciona tu Rol</h1>
            <p class="text-[0.95rem] text-[var(--surface-600)] m-0">
                Bienvenido, <span class="font-semibold text-[var(--primary-color)]">{{ username || 'Usuario' }}</span>. Elige una opción para ingresar.
            </p>
        </div>

        <Divider />

        <!-- Grid de roles -->
        <div v-if="roles && roles.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
            <RoleCard 
                v-for="role in roles" 
                :key="role.id" 
                :role="role"
                @select="$emit('select-role', role)"
            />
        </div>

        <!-- Estado vacío -->
        <div v-else class="text-center py-12 text-[var(--surface-500)] flex flex-col items-center gap-4">
            <i class="pi pi-exclamation-circle text-[2.5rem] text-[var(--surface-400)]"></i>
            <p>No se encontraron roles asignados a este usuario.</p>
        </div>
    </div>
</template>

<script setup>
import RoleCard from '@/components/cards/RoleCard.vue';

defineProps({
    roles: {
        type: Array,
        default: () => []
    },
    username: {
        type: String,
        default: ''
    }
});

defineEmits(['select-role']);
</script>