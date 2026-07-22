<template>
    <div 
        class="role-card" 
        @click="$emit('select', role)"
    >
        <div class="role-icon-container">
            <i :class="['pi', role.icon || 'pi-user']"></i>
        </div>
        
        <div class="role-info">
            <h3 class="role-name">{{ role.name }}</h3>
            <p class="role-desc">{{ role.description }}</p>
        </div>
    </div>
</template>

<script setup>
defineProps({
    role: {
        type: Object,
        required: true
    }
});

defineEmits(['select']);
</script>

<style scoped>
.role-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
    padding: 1rem 1rem;
    background: var(--surface-card);
    border: 1.5px solid var(--surface-300, #cbd5e1);
    border-radius: 10px; 
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.role-card:hover {
    border-color: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.role-icon-container {
    width: 4.5rem;
    height: 4.5rem;
    border-radius: 0px;
    background: var(--primary-50, rgba(var(--primary-color-rgb), 0.1));
    color: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.role-icon-container i {
    font-size: 2.25rem;
}

.role-info {
    width: 100%;
}

.role-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--surface-900);
    text-transform: capitalize;
    margin: 0 0 0.35rem 0;
}

.role-desc {
    font-size: 0.85rem;
    color: var(--surface-500);
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>