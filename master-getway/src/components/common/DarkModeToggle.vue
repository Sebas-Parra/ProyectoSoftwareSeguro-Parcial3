<template>
  <div class="toggle-dark-mode">
    <Button 
      @click="handleToggleDarkMode()" 
      severity="secondary" 
      size="large" 
      icon="pi pi-moon"
      :title="isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import { toggleDarkModeFacade } from '@/helpers/utils.js';

const isDark = ref(false);

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('my-app-dark');
});

const handleToggleDarkMode = () => {
  toggleDarkModeFacade();
  isDark.value = document.documentElement.classList.contains('my-app-dark');
};
</script>

<style scoped>
.toggle-dark-mode {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
