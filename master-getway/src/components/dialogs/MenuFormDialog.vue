<!-- components/dialogs/MenuFormDialog.vue -->
<template>
  <Dialog 
    :visible="visible" 
    :header="isEdit ? 'Editar Menú' : 'Crear Menú'" 
    :modal="true" 
    class="w-full max-w-[440px] mx-4"
    @update:visible="$emit('update:visible', $event)"
  >
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5 mt-2">
      <div class="flex flex-col gap-2">
        <label for="nombre" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-bars text-[var(--primary-color)]"></i> Nombre del Menú
        </label>
        <InputText id="nombre" v-model.trim="form.nombre" required autofocus class="w-full" placeholder="Ej: Configuración" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="url" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-link text-[var(--primary-color)]"></i> URL
        </label>
        <InputText id="url" v-model.trim="form.url" class="w-full" placeholder="Ej: /api/config" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="modulo_id" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-box text-[var(--primary-color)]"></i> ID del Módulo
        </label>
        <InputNumber id="modulo_id" v-model="form.modulo_id" required class="w-full" placeholder="Ej: 1" useGrouping="false" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="parent_id" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-sitemap text-[var(--primary-color)]"></i> ID Menú Padre (Opcional)
        </label>
        <InputNumber id="parent_id" v-model="form.parent_id" class="w-full" placeholder="Dejar vacío si es raíz" useGrouping="false" />
      </div>

      <div v-if="isEdit" class="flex items-center gap-2">
        <ToggleSwitch id="status" v-model="form.status" />
        <label for="status" class="font-semibold text-[var(--surface-900)]">Estado Activo</label>
      </div>

      <div class="flex justify-end gap-2 mt-4 pt-3">
        <Button type="button" label="Cancelar" icon="pi pi-times" severity="secondary" outlined @click="closeDialog" />
        <Button type="submit" label="Guardar" icon="pi pi-check" :loading="loading" />
      </div>
    </form>
  </Dialog>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import ToggleSwitch from 'primevue/toggleswitch';
import { useToastGlobal } from '@/helpers/utils.js';

const props = defineProps({
  visible: Boolean,
  menu: Object,
  allMenus: {
    type: Array,
    default: () => []
  },
  loading: Boolean
});

const emit = defineEmits(['update:visible', 'save']);
const { msjShow } = useToastGlobal();

const isEdit = ref(false);

const form = reactive({
  id: null,
  nombre: '',
  url: '',
  modulo_id: null,
  parent_id: null,
  status: true
});

watch(() => props.menu, (newMenu) => {
  if (newMenu) {
    isEdit.value = true;
    form.id = newMenu.id;
    form.nombre = newMenu.nombre || '';
    form.url = newMenu.url || '';
    form.modulo_id = newMenu.modulo_id ?? null;
    form.parent_id = newMenu.parent_id ?? null;
    form.status = newMenu.status ?? true;
  } else {
    isEdit.value = false;
    form.id = null;
    form.nombre = '';
    form.url = '';
    form.modulo_id = null;
    form.parent_id = null;
    form.status = true;
  }
}, { immediate: true });

const closeDialog = () => {
  emit('update:visible', false);
};

// Validación para evitar ciclos (cuando un menú se apunta a sí mismo o a uno de sus propios descendientes)
const hasCircularReference = (menuId, targetParentId, menusList) => {
  if (!targetParentId || !menuId) return false;
  if (targetParentId === menuId) return true;

  // Construir mapa de hijos para buscar hacia abajo
  const childrenMap = {};
  menusList.forEach(m => {
    if (m.parent_id) {
      if (!childrenMap[m.parent_id]) childrenMap[m.parent_id] = [];
      childrenMap[m.parent_id].push(m.id);
    }
  });

  // Recorrido BFS/DFS para ver si menuId está en la descendencia de targetParentId
  const queue = [targetParentId];
  const visited = new Set();

  while (queue.length > 0) {
    const currentId = queue.shift();
    if (currentId === menuId) return true;
    if (!visited.has(currentId)) {
      visited.add(currentId);
      const kids = childrenMap[currentId] || [];
      for (const kidId of kids) {
        queue.push(kidId);
      }
    }
  }

  return false;
};

const handleSubmit = () => {
  // Validar autorreferencia directa
  if (isEdit.value && form.parent_id === form.id) {
    msjShow('error', 'Error de Validación', 'Un menú no puede ser padre de sí mismo.', 4000);
    return;
  }

  // Validar referencia cíclica profunda si se cuenta con la lista total de menús
  if (isEdit.value && form.parent_id && props.allMenus && props.allMenus.length > 0) {
    if (hasCircularReference(form.id, form.parent_id, props.allMenus)) {
      msjShow('error', 'Error de Validación', 'Referencia cíclica detectada: Un menú no puede depender de uno de sus propios submenús.', 4000);
      return;
    }
  }

  emit('save', { ...form }, isEdit.value);
};
</script>