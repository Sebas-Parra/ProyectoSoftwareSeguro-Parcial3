<!-- components/dialogs/RoleUserAssignmentDialog.vue -->
<template>
  <Dialog 
    :visible="visible" 
    :header="`Asignar Usuarios a: ${role?.name || ''}`" 
    :modal="true" 
    class="w-full max-w-[480px] mx-4"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="flex flex-col gap-4 mt-2">
      <!-- Asignar Usuario -->
      <div class="flex flex-col gap-2">
        <label for="userSelect" class="font-semibold text-[var(--surface-900)]">Seleccionar Usuario</label>
        <div class="flex gap-2">
          <Select 
            id="userSelect" 
            v-model="selectedUserId" 
            :options="users" 
            optionLabel="username" 
            optionValue="id" 
            placeholder="Seleccione un usuario" 
            class="w-full"
            filter
            :loading="loadingUsers"
          />
          <Button label="Asignar" icon="pi pi-user-plus" @click="handleAssign" :loading="loadingAssign" :disabled="!selectedUserId" />
        </div>
      </div>

      <Divider />

      <!-- Remover Usuario -->
      <div class="flex flex-col gap-2">
        <label for="removeUserSelect" class="font-semibold text-[var(--surface-900)]">Remover Usuario de este Rol</label>
        <div class="flex gap-2">
          <Select 
            id="removeUserSelect" 
            v-model="selectedRemoveId" 
            :options="users" 
            optionLabel="username" 
            optionValue="id" 
            placeholder="Seleccione un usuario" 
            class="w-full"
            filter
            :loading="loadingUsers"
          />
          <Button label="Remover" icon="pi pi-user-minus" severity="danger" outlined @click="handleRemove" :loading="loadingRemove" :disabled="!selectedRemoveId" />
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import Dialog from 'primevue/dialog';
import Select from 'primevue/select';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import { roleService } from '@/services/roleService.js';
import { userService } from '@/services/userService.js';
import { useToastGlobal } from '@/helpers/utils.js';

const props = defineProps({
  visible: Boolean,
  role: Object
});

const emit = defineEmits(['update:visible']);
const { msjShow } = useToastGlobal();

const users = ref([]);
const selectedUserId = ref(null);
const selectedRemoveId = ref(null);
const loadingUsers = ref(false);
const loadingAssign = ref(false);
const loadingRemove = ref(false);

// Cargar la lista de usuarios al abrir el diálogo
const fetchAllUsers = async () => {
  loadingUsers.value = true;
  try {
    const { data } = await userService.getUsers(1, 100);
    users.value = data.data || data;
  } catch (error) {
    console.error("Error al cargar la lista de usuarios:", error);
    msjShow('error', 'Error', 'No se pudo cargar la lista de usuarios', 3000);
  } finally {
    loadingUsers.value = false;
  }
};

watch(() => props.visible, (val) => {
  if (val) {
    selectedUserId.value = null;
    selectedRemoveId.value = null;
    fetchAllUsers();
  }
});

const handleAssign = async () => {
  if (!selectedUserId.value || !props.role) return;
  loadingAssign.value = true;
  try {
    await roleService.assignRoleToUser(props.role.id, selectedUserId.value);
    msjShow('success', 'Éxito', 'Rol asignado correctamente al usuario', 3000);
    selectedUserId.value = null;
  } catch (error) {
    console.error("Error al asignar rol al usuario:", error);
    msjShow('error', 'Error', error.response?.data?.detail || 'No se pudo asignar el rol', 4000);
  } finally {
    loadingAssign.value = false;
  }
};

const handleRemove = async () => {
  if (!selectedRemoveId.value || !props.role) return;
  loadingRemove.value = true;
  try {
    await roleService.removeRoleFromUser(props.role.id, selectedRemoveId.value);
    msjShow('success', 'Éxito', 'Rol removido correctamente del usuario', 3000);
    selectedRemoveId.value = null;
  } catch (error) {
    console.error("Error al desasignar rol del usuario:", error);
    msjShow('error', 'Error', error.response?.data?.detail || 'No se pudo remover el rol', 4000);
  } finally {
    loadingRemove.value = false;
  }
};
</script>