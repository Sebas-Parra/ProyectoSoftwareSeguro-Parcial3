<!-- components/dialogs/RoleFormDialog.vue -->
<template>
  <Dialog 
    :visible="visible" 
    :header="isEdit ? 'Editar Rol' : 'Crear Rol'" 
    :modal="true" 
    class="w-full max-w-[440px] mx-4"
    @update:visible="$emit('update:visible', $event)"
  >
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5 mt-2">
      <div class="flex flex-col gap-2">
        <label for="name" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-shield text-[var(--primary-color)]"></i> Nombre del Rol
        </label>
        <InputText id="name" v-model.trim="form.name" required autofocus class="w-full" placeholder="Ej: Administrador" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="description" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-file-edit text-[var(--primary-color)]"></i> Descripción
        </label>
        <InputText id="description" v-model.trim="form.description" class="w-full" placeholder="Breve descripción del rol" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="icon" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-icons text-[var(--primary-color)]"></i> Icono (PrimeIcons)
        </label>
        <InputText id="icon" v-model.trim="form.icon" class="w-full" placeholder="Ej: pi pi-user" />
      </div>

      <div class="flex items-center gap-2">
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
import Button from 'primevue/button';
import ToggleSwitch from 'primevue/toggleswitch';

const props = defineProps({
  visible: Boolean,
  role: Object,
  loading: Boolean
});

const emit = defineEmits(['update:visible', 'save']);

const isEdit = ref(false);

const form = reactive({
  id: null,
  name: '',
  description: '',
  icon: '',
  status: true
});

watch(() => props.role, (newRole) => {
  if (newRole) {
    isEdit.value = true;
    form.id = newRole.id;
    form.name = newRole.name || '';
    form.description = newRole.description || '';
    form.icon = newRole.icon || '';
    form.status = newRole.status ?? true;
  } else {
    isEdit.value = false;
    form.id = null;
    form.name = '';
    form.description = '';
    form.icon = '';
    form.status = true;
  }
}, { immediate: true });

const closeDialog = () => {
  emit('update:visible', false);
};

const handleSubmit = () => {
  emit('save', { ...form }, isEdit.value);
};
</script>