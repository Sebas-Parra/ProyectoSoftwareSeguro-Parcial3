<!-- components/tables/MenuTable.vue -->
<template>
  <DataTable 
    :value="menus" 
    :loading="loading"
    paginator
    :rows="5"
    dataKey="id"
    tableStyle="min-width: 50rem"
  >
    <Column field="id" header="ID"></Column>
    <Column field="nombre" header="Nombre"></Column>
    <Column field="url" header="URL">
      <template #body="slotProps">
        {{ slotProps.data.url || 'Sin URL' }}
      </template>
    </Column>
    <Column field="modulo_id" header="ID Módulo"></Column>
    <Column field="parent_id" header="ID Padre">
      <template #body="slotProps">
        {{ slotProps.data.parent_id !== null ? slotProps.data.parent_id : 'Raíz' }}
      </template>
    </Column>
    <Column field="status" header="Estado">
      <template #body="slotProps">
        <Tag :value="slotProps.data.status ? 'Activo' : 'Inactivo'" :severity="slotProps.data.status ? 'success' : 'danger'" />
      </template>
    </Column>
    <Column header="Acciones" style="width: 20%">
      <template #body="slotProps">
        <div class="flex gap-2">
          <Button icon="pi pi-shield" severity="info" rounded v-tooltip.top="'Asignar a Rol'" @click="$emit('manage-roles', slotProps.data)" />
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
  menus: Array,
  loading: Boolean
});

defineEmits(['edit', 'delete', 'manage-roles']);
</script>