<template>
    <div class="page-layout">
        <SelectRoleContainer 
            :roles="user?.roles" 
            :username="user?.username"
            @select-role="handleRoleSelect"
        />
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuth } from '@/helpers/useAuth.js';
import SelectRoleContainer from '@/components/containers/SelectRoleContainer.vue';

const emit = defineEmits(['select-role']);
const { user } = useAuth();

const activeRole = computed({
    get: () => {
        const storedRole = localStorage.getItem('activeRole');
        return storedRole ? JSON.parse(storedRole) : null;
    },
    set: (role) => {
        if (role) {
            localStorage.setItem('activeRole', JSON.stringify(role));
        } else {
            localStorage.removeItem('activeRole');
        }
    }
});

const handleRoleSelect = (role) => {
    activeRole.value = role;
    emit('select-role', role);
};
</script>

<style scoped>
.page-layout {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}
</style>