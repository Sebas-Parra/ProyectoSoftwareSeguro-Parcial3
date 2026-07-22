<!-- components/dialogs/SaleFormDialog.vue -->
<template>
  <Dialog 
    :visible="visible" 
    :header="isEdit ? 'Editar Venta' : 'Crear Venta'" 
    :modal="true" 
    class="w-full max-w-[440px] mx-4"
    @update:visible="$emit('update:visible', $event)"
  >
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5 mt-2">
      <div class="flex flex-col gap-2">
        <label for="name" class="font-semibold text-[var(--surface-900)]">Nombre</label>
        <InputText id="name" type="text" v-model="form.name" required autofocus class="w-full" placeholder="Nombre de la venta" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="description" class="font-semibold text-[var(--surface-900)]">Descripción</label>
        <InputText id="description" type="text" v-model="form.description" class="w-full" placeholder="Detalle opcional" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="total" class="font-semibold text-[var(--surface-900)]">Total</label>
        <InputText id="total" type="number" step="0.01" v-model.number="form.total" required class="w-full" placeholder="0.00" />
      </div>

      <div class="flex items-center gap-2">
        <ToggleSwitch id="status" v-model="form.status" />
        <label for="status" class="font-semibold text-[var(--surface-900)]">Estado Completado</label>
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
  sale: Object,
  loading: Boolean
});

const emit = defineEmits(['update:visible', 'save']);

const isEdit = ref(false);

const form = reactive({
  id: null,
  name: '',
  description: '',
  total: 0,
  status: true
});

watch(() => props.sale, (newSale) => {
  if (newSale) {
    isEdit.value = true;
    form.id = newSale.id;
    form.name = newSale.name ?? '';
    form.description = newSale.description ?? '';
    form.total = newSale.total ?? 0;
    form.status = newSale.status ?? true;
  } else {
    isEdit.value = false;
    form.id = null;
    form.name = '';
    form.description = '';
    form.total = 0;
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