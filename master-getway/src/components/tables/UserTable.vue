<template>
  <DataTable 
    :value="users" 
    lazy 
    paginator 
    :rows="limit" 
    :totalRecords="totalRecords" 
    :loading="loading"
    @page="onPageChange"
    dataKey="id"
    tableStyle="min-width: 50rem"
  >
    <Column field="username" header="Usuario"></Column>
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
    <Column header="Acciones" style="width: 15%">
      <template #body="slotProps">
        <div class="flex gap-2">
          <Button icon="pi pi-pencil" severity="warn" rounded @click="$emit('edit', slotProps.data)" />
          <Button icon="pi pi-trash" severity="danger" rounded @click="$emit('delete', slotProps.data.id)" />
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
  users: Array,
  totalRecords: Number,
  limit: Number,
  loading: Boolean
});

const emit = defineEmits(['page-change', 'edit', 'delete']);

const onPageChange = (event) => {
  // PrimeVue entrega el índice 'page' comenzando en 0, lo adaptamos a base 1 para FastAPI
  const page = event.page + 1; 
  emit('page-change', page);
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString();
};
</script>