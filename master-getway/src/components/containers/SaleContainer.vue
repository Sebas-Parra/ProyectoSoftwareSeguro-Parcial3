<!-- components/containers/SaleContainer.vue -->
<template>
  <div class="card p-4">    
    <!-- Barra Superior con Botón Crear -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Gestión de Ventas</h2>
      <Button label="Nueva Venta" icon="pi pi-plus" @click="openCreateModal" />
    </div>

    <!-- Tabla -->
    <SaleTable 
      :sales="sales" 
      :loading="loading"
      @edit="openEditModal"
      @delete="confirmDelete"
    />

    <!-- Modal Formulario CRUD -->
    <SaleFormDialog 
      v-model:visible="dialogVisible" 
      :sale="selectedSale" 
      :loading="saving"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import { useConfirm } from "primevue/useconfirm";
import SaleTable from '@/components/tables/SaleTable.vue';
import SaleFormDialog from '@/components/dialogs/SaleFormDialog.vue';
import { saleService } from '@/services/saleService.js';
import { useToastGlobal } from '@/helpers/utils.js';

const confirm = useConfirm();
const { msjShow } = useToastGlobal();

const sales = ref([]);
const loading = ref(false);

const dialogVisible = ref(false);
const selectedSale = ref(null);
const saving = ref(false);

// components/containers/SaleContainer.vue
const fetchSales = async () => {
  loading.value = true;    
  try {
    const response = await saleService.getSales();
    
    // Como tu API responde: { data: [...], page: 1, limit: 5, total: 1, ... }
    // Y saleService ya devuelve response.data, evaluamos la propiedad .data
    if (response && Array.isArray(response.data)) {
      sales.value = response.data;
    } else if (Array.isArray(response)) {
      sales.value = response;
    } else {
      sales.value = [];
    }
  } catch (error) {
    console.error("Error al cargar ventas:", error);
    msjShow('error', 'Error', 'No se pudieron cargar las ventas', 3000);
    sales.value = [];
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  selectedSale.value = null;
  dialogVisible.value = true;
};

const openEditModal = (sale) => {
  selectedSale.value = { ...sale };
  dialogVisible.value = true;
};

const handleSave = async (formData, isEdit) => {
  saving.value = true;
  try {
    const payload = {
      name: formData.name,
      description: formData.description,
      total: formData.total,
      status: formData.status
    };

    if (isEdit) {
      await saleService.updateSale(formData.id, payload);
      msjShow('success', 'Éxito', 'Venta actualizada correctamente', 3000);
    } else {
      await saleService.createSale(payload);
      msjShow('success', 'Éxito', 'Venta creada correctamente', 3000);
    }
    dialogVisible.value = false;
    fetchSales();
  } catch (error) {
    console.error("Error guardando la venta:", error);
    msjShow('error', 'Error', error.response?.data?.detail || 'No se pudo guardar la venta', 4000);
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (saleId) => {
    confirm.require({
        message: '¿Está seguro de que desea eliminar esta venta?',
        header: 'Confirmar Eliminación',
        icon: 'pi pi-exclamation-circle',
        acceptProps: { label: 'Eliminar', severity: 'danger' },
        rejectProps: { label: 'Cancelar', severity: 'secondary', outlined: true },
        accept: async () => {
            try {
                await saleService.deleteSale(saleId);
                msjShow('success', 'Éxito', 'Venta eliminada correctamente', 3000);
                fetchSales();
            } catch (error) {
                console.error("Error al eliminar la venta:", error);
                msjShow('error', 'Error', 'No se pudo eliminar la venta', 4000);
            }
        }
    });
};

onMounted(() => {
  fetchSales();
});
</script>