<!-- components/tables/ModuleTable.vue -->
<template>
  <DataTable 
    :value="modules" 
    :loading="loading"
    dataKey="id"
    tableStyle="min-width: 50rem"
  >
    <Column field="id" header="ID"></Column>
    <Column field="name" header="Nombre del Módulo"></Column>
    <Column field="description" header="Descripción">
      <template #body="slotProps">
        {{ slotProps.data.description || 'Sin descripción' }}
      </template>
    </Column>
    <Column field="created_at" header="Fecha de Creación">
      <template #body="slotProps">
        {{ formatDate(slotProps.data.created_at) }}
      </template>
    </Column>
    <Column field="updated_at" header="Última Actualización">
      <template #body="slotProps">
        {{ formatDate(slotProps.data.updated_at) }}
      </template>
    </Column>
    <Column field="status" header="Estado">
      <template #body="slotProps">
        <Tag :value="slotProps.data.status === true ? 'Activo' : 'Inactivo'" :severity="slotProps.data.status === true ? 'success' : 'danger'" />
      </template>
    </Column>
    <Column header="Acciones" style="width: 20%">
      <template #body="slotProps">
        <div class="flex gap-2">
          <!-- Botón para gestionar roles de este módulo -->
          <Button icon="pi pi-shield" severity="info" rounded v-tooltip.top="'Gestionar Roles'" @click="$emit('manage-roles', slotProps.data)" />
          <Button icon="pi pi-pencil" severity="warn" rounded v-tooltip.top="'Editar'" @click="$emit('edit', slotProps.data)" />
          <Button icon="pi pi-trash" severity="danger" rounded v-tooltip.top="'Eliminar'" @click="$emit('delete', slotProps.data.id)" />
        </div>
      </template>
    </Column>
  </DataTable>
</template>

<script setup>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';

defineProps({
  modules: Array,
  loading: Boolean
});

defineEmits(['edit', 'delete', 'manage-roles']);

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString();
};
</script>