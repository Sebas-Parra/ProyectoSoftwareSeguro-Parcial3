<!-- components/containers/MenuContainer.vue -->
<template>
  <div class="card p-4">
    
    <!-- Barra Superior con Botón Crear -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Gestión de Menús</h2>
      <Button label="Nuevo Menú" icon="pi pi-plus" @click="openCreateModal" />
    </div>

    <!-- Tabla Estándar -->
    <MenuTable 
      :menus="menus" 
      :loading="loading"
      @edit="openEditModal"
      @delete="confirmDelete"
      @manage-roles="openAssignmentModal"
    />

    <!-- Modal Formulario CRUD -->
    <MenuFormDialog 
      v-model:visible="dialogVisible" 
      :menu="selectedMenu" 
      :loading="saving"
      @save="handleSave"
    />

    <!-- Modal de Asignación de Roles por Menú -->
    <MenuRoleAssignmentDialog
      v-model:visible="assignmentDialogVisible"
      :menu="selectedMenu"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from "primevue/useconfirm";
import MenuTable from '@/components/tables/MenuTable.vue';
import MenuFormDialog from '@/components/dialogs/MenuFormDialog.vue';
import MenuRoleAssignmentDialog from '@/components/dialogs/MenuRoleAssignmentDialog.vue';
import { menuService } from '@/services/menuService.js';

const confirm = useConfirm();

const menus = ref([]);
const loading = ref(false);

const dialogVisible = ref(false);
const assignmentDialogVisible = ref(false);
const selectedMenu = ref(null);
const saving = ref(false);

const fetchMenus = async () => {
  loading.value = true;    
  try {
    const { data } = await menuService.getMenus();
    menus.value = Array.isArray(data) ? data : data.data; 
  } catch (error) {
    console.error("Error al cargar menús:", error);
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  selectedMenu.value = null;
  dialogVisible.value = true;
};

const openEditModal = (menuItem) => {
  selectedMenu.value = { ...menuItem };
  dialogVisible.value = true;
};

const openAssignmentModal = (menuItem) => {
  selectedMenu.value = menuItem;
  assignmentDialogVisible.value = true;
};

const handleSave = async (formData, isEdit) => {
  saving.value = true;
  try {
    if (isEdit) {
      const updatePayload = {
        nombre: formData.nombre,
        url: formData.url || null,
        parent_id: formData.parent_id !== undefined ? formData.parent_id : null,
        status: formData.status
      };
      await menuService.updateMenu(formData.id, updatePayload);
    } else {
      const createPayload = {
        nombre: formData.nombre,
        url: formData.url || null,
        modulo_id: formData.modulo_id,
        parent_id: formData.parent_id !== undefined ? formData.parent_id : null
      };
      await menuService.createMenu(createPayload);
    }
    dialogVisible.value = false;
    fetchMenus();
  } catch (error) {
    console.error("Error guardando el menú:", error);
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (menuId) => {
    confirm.require({
        message: '¿Está seguro de que desea eliminar este menú?',
        header: 'Confirmar Eliminación',
        icon: 'pi pi-exclamation-circle',
        acceptProps: { label: 'Eliminar', severity: 'danger' },
        rejectProps: { label: 'Cancelar', severity: 'secondary', outlined: true },
        accept: async () => {
            try {
                await menuService.deleteMenu(menuId);
                fetchMenus();
            } catch (error) {
                console.error("Error al eliminar el menú:", error);
            }
        }
    });
};

onMounted(() => {
  fetchMenus();
});
</script>