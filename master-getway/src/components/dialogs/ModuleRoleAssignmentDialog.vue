<!-- components/dialogs/ModuleRoleAssignmentDialog.vue -->
<template>
  <Dialog 
    :visible="visible" 
    :header="`Asignar Roles a Módulo: ${moduleData?.name || ''}`" 
    :modal="true" 
    class="w-full max-w-[480px] mx-4"
    @update:visible="$emit('update:visible', $event)"
  >
    <div class="flex flex-col gap-4 mt-2">
      <!-- Asignar Rol -->
      <div class="flex flex-col gap-2">
        <label for="roleSelect" class="font-semibold text-[var(--surface-900)]">Seleccionar Rol</label>
        <div class="flex gap-2">
          <Select 
            id="roleSelect" 
            v-model="selectedRoleId" 
            :options="roles" 
            optionLabel="name" 
            optionValue="id" 
            placeholder="Seleccione un rol" 
            class="w-full"
            filter
            :loading="loadingRoles"
          />
          <Button label="Asignar" icon="pi pi-shield" @click="handleAssign" :loading="loadingAssign" :disabled="!selectedRoleId" />
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
import { moduleService } from '@/services/moduleService.js';
import { roleService } from '@/services/roleService.js';
import { useToastGlobal } from '@/helpers/utils.js';

const props = defineProps({
  visible: Boolean,
  moduleData: Object
});

const emit = defineEmits(['update:visible']);
const { msjShow } = useToastGlobal();

const roles = ref([]);
const selectedRoleId = ref(null);
const loadingRoles = ref(false);
const loadingAssign = ref(false);

const fetchAllRoles = async () => {
  loadingRoles.value = true;
  try {
    const { data } = await roleService.getRoles();
    roles.value = Array.isArray(data) ? data : data.data;
  } catch (error) {
    console.error("Error al cargar la lista de roles:", error);
    msjShow('error', 'Error', 'No se pudo cargar la lista de roles', 3000);
  } finally {
    loadingRoles.value = false;
  }
};

watch(() => props.visible, (val) => {
  if (val) {
    selectedRoleId.value = null;
    fetchAllRoles();
  }
});

const handleAssign = async () => {
  if (!selectedRoleId.value || !props.moduleData) return;
  loadingAssign.value = true;
  try {
    await moduleService.assignModuleToRole(props.moduleData.id, selectedRoleId.value);
    msjShow('success', 'Éxito', 'Rol asignado correctamente al módulo', 3000);
    selectedRoleId.value = null;
  } catch (error) {
    console.error("Error al asignar rol al módulo:", error);
    msjShow('error', 'Error', error.response?.data?.detail || 'No se pudo asignar el rol', 4000);
  } finally {
    loadingAssign.value = false;
  }
};
</script>