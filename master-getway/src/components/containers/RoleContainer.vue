<!-- components/RoleContainer.vue -->
<template>
  <div class="card p-4">    
    <!-- Barra Superior con Botón Crear -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Gestión de Roles</h2>
      <Button label="Nuevo Rol" icon="pi pi-plus" @click="openCreateModal" />
    </div>

    <!-- Tabla -->
    <RoleTable 
      :roles="roles" 
      :loading="loading"
      @edit="openEditModal"
      @delete="confirmDelete"
      @manage-users="openAssignmentModal"
    />

    <!-- Modal Formulario CRUD -->
    <RoleFormDialog 
      v-model:visible="dialogVisible" 
      :role="selectedRole" 
      :loading="saving"
      @save="handleSave"
    />

    <!-- Modal de Asignación de Roles por Usuario -->
    <RoleUserAssignmentDialog
      v-model:visible="assignmentDialogVisible"
      :role="selectedRole"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from "primevue/useconfirm";
import RoleTable from '@/components/tables/RoleTable.vue';
import RoleFormDialog from '@/components/dialogs/RoleFormDialog.vue';
import RoleUserAssignmentDialog from '@/components/dialogs/RoleUserAssignmentDialog.vue';
import { roleService } from '@/services/roleService.js';

const confirm = useConfirm();

const roles = ref([]);
const loading = ref(false);

const dialogVisible = ref(false);
const assignmentDialogVisible = ref(false);
const selectedRole = ref(null);
const saving = ref(false);

const fetchRoles = async () => {
  loading.value = true;     
  try {
    const { data } = await roleService.getRoles();
    roles.value = Array.isArray(data) ? data : data.data; 
  } catch (error) {
    console.error("Error al cargar roles:", error);
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  selectedRole.value = null;
  dialogVisible.value = true;
};

const openEditModal = (role) => {
  selectedRole.value = { ...role };
  dialogVisible.value = true;
};

const openAssignmentModal = (role) => {
  selectedRole.value = role;
  assignmentDialogVisible.value = true;
};

const handleSave = async (formData, isEdit) => {
  saving.value = true;
  try {
    // Incluimos icon y status en el payload que espera FastAPI (RoleDTO)
    const payload = {
      name: formData.name,
      description: formData.description,
      icon: formData.icon,
      status: formData.status
    };

    if (isEdit) {
      await roleService.updateRole(formData.id, payload);
    } else {
      await roleService.createRole(payload);
    }
    dialogVisible.value = false;
    fetchRoles();
  } catch (error) {
    console.error("Error guardando el rol:", error);
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (roleId) => {
    confirm.require({
        message: '¿Está seguro de que desea eliminar este rol?',
        header: 'Confirmar Eliminación',
        icon: 'pi pi-exclamation-circle',
        acceptProps: { label: 'Eliminar', severity: 'danger' },
        rejectProps: { label: 'Cancelar', severity: 'secondary', outlined: true },
        accept: async () => {
            try {
                await roleService.deleteRole(roleId);
                fetchRoles();
            } catch (error) {
                console.error("Error al eliminar el rol:", error);
            }
        }
    });
};

onMounted(() => {
  fetchRoles();
});
</script>