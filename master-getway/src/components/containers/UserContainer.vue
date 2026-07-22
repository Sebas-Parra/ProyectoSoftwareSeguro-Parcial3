<template>
  <div class="card p-4">
    <!-- Barra Superior con Botón Crear -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Gestión de Usuarios</h2>
      <Button label="Nuevo Usuario" icon="pi pi-plus" @click="openCreateModal" />
    </div>

    <!-- Tabla -->
    <UserTable 
      :users="users" 
      :totalRecords="total" 
      :limit="limit" 
      :loading="loading"
      @page-change="handlePageChange"
      @edit="openEditModal"
      @delete="confirmDelete"
    />

    <!-- Modal Formulario -->
    <UserFormDialog 
      v-model:visible="dialogVisible" 
      :user="selectedUser" 
      :loading="saving"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from "primevue/useconfirm";
import UserTable from '@/components/tables/UserTable.vue';
import UserFormDialog from '@/components/dialogs/UserFormDialog.vue';
import { userService } from '@/services/userService.js';

const confirm = useConfirm();

// Estados de la Tabla
const users = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(10);
const loading = ref(false);

// Estados del Dialog
const dialogVisible = ref(false);
const selectedUser = ref(null);
const saving = ref(false);

// 1. Cargar Usuarios
const fetchUsers = async () => {
  loading.value = true;     
  try {
    const { data } = await userService.getUsers(page.value, limit.value);
    users.value = data.data;
    total.value = data.total;
  } catch (error) {
    console.error("Error al cargar usuarios:", error);
  } finally {
    loading.value = false;
  }
};

// 2. Control de Paginación
const handlePageChange = (newPage) => {
  page.value = newPage;
  fetchUsers();
};

// 3. Abrir Modales
const openCreateModal = () => {
  selectedUser.value = null;
  dialogVisible.value = true;
};

const openEditModal = (user) => {
  selectedUser.value = { ...user };
  dialogVisible.value = true;
};

// 4. Guardar (Crear o Editar)
const handleSave = async (formData, isEdit) => {
  saving.value = true;
  try {
    if (isEdit) {
      await userService.updateUser(formData.id, {
        username: formData.username,
        password: formData.password
      });
    } else {
      await userService.createUser({
        username: formData.username,
        password: formData.password
      });
    }
    dialogVisible.value = false;
    fetchUsers(); // Recargar lista
  } catch (error) {
    console.error("Error guardando el usuario:", error);
  } finally {
    saving.value = false;
  }
};

// 5. Confirmar y Eliminar
const confirmDelete = (userId) => {
    confirm.require({
        message: '¿Está seguro de que desea eliminar este usuario?',
        header: 'Confirmar Eliminación',
        icon: 'pi pi-exclamation-circle',
        acceptProps: { label: 'Eliminar', severity: 'danger' },
        rejectProps: { label: 'Cancelar', severity: 'secondary', outlined: true },
        accept: async () => {
            try {
                await userService.deleteUser(userId);
                fetchUsers();
            } catch (error) {
                console.error("Error al eliminar el usuario:", error);
            }
        }
    });
};

onMounted(() => {
  fetchUsers();
});
</script>