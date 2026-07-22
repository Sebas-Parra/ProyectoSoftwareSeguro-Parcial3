<!-- components/tables/SaleTable.vue -->
<template>
  <DataTable 
    :value="sales" 
    :loading="loading"
    dataKey="id"
    tableStyle="min-width: 50rem"
  >
    <Column field="id" header="ID"></Column>
    <Column field="name" header="Nombre"></Column>
    <Column field="description" header="Descripción">
      <template #body="slotProps">
        {{ slotProps.data.description || 'Sin descripción' }}
      </template>
    </Column>
    <Column field="total" header="Total">
      <template #body="slotProps">
        {{ formatCurrency(slotProps.data.total) }}
      </template>
    </Column>
    <Column field="created_at" header="Fecha de Creación">
      <template #body="slotProps">
        {{ formatDate(slotProps.data.created_at) }}
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
          <Button icon="pi pi-pencil" severity="warn" rounded  @click="$emit('edit', slotProps.data)" />
          <Button icon="pi pi-trash" severity="danger" rounded  @click="$emit('delete', slotProps.data.id)" />
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
  sales: Array,
  loading: Boolean
});

defineEmits(['edit', 'delete']);

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString();
};

const formatCurrency = (value) => {
  if (value === undefined || value === null) return '$0.00';
  return Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' });
};
</script>