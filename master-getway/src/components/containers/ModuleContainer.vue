<!-- components/containers/ModuleContainer.vue -->
<template>
  <div class="card p-4">    
    <!-- Barra Superior con Botón Crear -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Gestión de Módulos</h2>
      <Button label="Nuevo Módulo" icon="pi pi-plus" @click="openCreateModal" />
    </div>

    <!-- Tabla -->
    <ModuleTable 
      :modules="modules" 
      :loading="loading"
      @edit="openEditModal"
      @delete="confirmDelete"
      @manage-roles="openAssignmentModal"
    />

    <!-- Modal Formulario CRUD -->
    <ModuleFormDialog 
      v-model:visible="dialogVisible" 
      :moduleData="selectedModule" 
      :loading="saving"
      @save="handleSave"
    />

    <!-- Modal de Asignación de Roles por Módulo -->
    <ModuleRoleAssignmentDialog
      v-model:visible="assignmentDialogVisible"
      :moduleData="selectedModule"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import { useConfirm } from "primevue/useconfirm";
import ModuleTable from '@/components/tables/ModuleTable.vue';
import ModuleFormDialog from '@/components/dialogs/ModuleFormDialog.vue';
import ModuleRoleAssignmentDialog from '@/components/dialogs/ModuleRoleAssignmentDialog.vue';
import { moduleService } from '@/services/moduleService.js';

const confirm = useConfirm();

const modules = ref([]);
const loading = ref(false);

const dialogVisible = ref(false);
const assignmentDialogVisible = ref(false);
const selectedModule = ref(null);
const saving = ref(false);

const fetchModules = async () => {
  loading.value = true;    
  try {
    const { data } = await moduleService.getModules();
    modules.value = Array.isArray(data) ? data : data.data; 
  } catch (error) {
    console.error("Error al cargar módulos:", error);
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  selectedModule.value = null;
  dialogVisible.value = true;
};

const openEditModal = (moduleItem) => {
  selectedModule.value = { ...moduleItem };
  dialogVisible.value = true;
};

const openAssignmentModal = (moduleItem) => {
  selectedModule.value = moduleItem;
  assignmentDialogVisible.value = true;
};

const handleSave = async (formData, isEdit) => {
  saving.value = true;
  try {
    const payload = {
      name: formData.name,
      description: formData.description,
      icon: formData.icon,
      status: formData.status
    };

    if (isEdit) {
      await moduleService.updateModule(formData.id, payload);
    } else {
      await moduleService.createModule(payload);
    }
    dialogVisible.value = false;
    fetchModules();
  } catch (error) {
    console.error("Error guardando el módulo:", error);
  } finally {
    saving.value = false;
  }
};

const confirmDelete = (moduleId) => {
    confirm.require({
        message: '¿Está seguro de que desea eliminar este módulo?',
        header: 'Confirmar Eliminación',
        icon: 'pi pi-exclamation-circle',
        acceptProps: { label: 'Eliminar', severity: 'danger' },
        rejectProps: { label: 'Cancelar', severity: 'secondary', outlined: true },
        accept: async () => {
            try {
                await moduleService.deleteModule(moduleId);
                fetchModules();
            } catch (error) {
                console.error("Error al eliminar el módulo:", error);
            }
        }
    });
};

onMounted(() => {
  fetchModules();
});
</script>