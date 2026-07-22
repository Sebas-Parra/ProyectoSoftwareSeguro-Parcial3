<template>
  <Dialog 
    :visible="visible" 
    :header="isEdit ? 'Editar Usuario' : 'Crear Usuario'" 
    :modal="true" 
    class="w-full max-w-[440px] mx-4"
    @update:visible="$emit('update:visible', $event)"
  >
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5 mt-2">
      <div class="flex flex-col gap-2">
        <label for="username" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-user text-[var(--primary-color)]"></i> Usuario
        </label>
        <InputText id="username" v-model.trim="form.username" required autofocus class="w-full" placeholder="Ingrese el nombre de usuario" />
      </div>

      <div class="flex flex-col gap-2">
        <label for="password" class="font-semibold text-[var(--surface-900)] flex items-center gap-2">
          <i class="pi pi-lock text-[var(--primary-color)]"></i> 
          {{ isEdit ? 'Nueva Contraseña (Opcional)' : 'Contraseña' }}
        </label>
        <Password 
          id="password" 
          v-model="form.password" 
          :toggleMask="true" 
          :feedback="true" 
          :required="!isEdit" 
          inputClass="w-full" 
          class="w-full" 
          placeholder="••••••••"
        >
          <template #header>
            <div class="font-semibold mb-2">Sugiere una contraseña segura</div>
          </template>
          <template #footer>
            <Divider />
            <ul class="pl-2 ml-2 mt-0" style="line-height: 1.5">
              <li>Mínimo 12 caracteres</li>
              <li>Al menos una letra minúscula</li>
              <li>Al menos una letra mayúscula</li>
              <li>Al menos un número</li>
              <li>Al menos un símbolo especial</li>
            </ul>
          </template>
        </Password>
        <small v-if="passwordError" class="text-red-500">{{ passwordError }}</small>
      </div>

      <div class="flex justify-end gap-2 mt-4 pt-3">
        <Button type="button" label="Cancelar" icon="pi pi-times" severity="secondary" outlined @click="closeDialog" />
        <Button type="submit" label="Guardar" icon="pi pi-check" :loading="loading" />
      </div>
    </form>
  </Dialog>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Divider from 'primevue/divider';

const props = defineProps({
  visible: Boolean,
  user: Object,
  loading: Boolean
});

const emit = defineEmits(['update:visible', 'save']);

const isEdit = reactive({ value: false });
const passwordError = ref('');

const form = reactive({
  id: null,
  username: '',
  password: ''
});

watch(() => props.user, (newUser) => {
  passwordError.value = '';
  if (newUser) {
    isEdit.value = true;
    form.id = newUser.id;
    form.username = newUser.username;
    form.password = '';
  } else {
    isEdit.value = false;
    form.id = null;
    form.username = '';
    form.password = '';
  }
}, { immediate: true });

const closeDialog = () => {
  passwordError.value = '';
  emit('update:visible', false);
};

const validatePassword = (pass, isEditing) => {
  if (isEditing && !pass) return true; // En edición la contraseña es opcional
  if (!pass) return false;
  
  const minLength = pass.length >= 12;
  const hasLower = /[a-z]/.test(pass);
  const hasUpper = /[A-Z]/.test(pass);
  const hasNumber = /\d/.test(pass);
  const hasSpecial = /[\W_]/.test(pass);

  return minLength && hasLower && hasUpper && hasNumber && hasSpecial;
};

const handleSubmit = () => {
  passwordError.value = '';

  if (!isEdit.value && !form.password) {
    passwordError.value = 'La contraseña es obligatoria.';
    return;
  }

  if (form.password && !validatePassword(form.password, isEdit.value)) {
    passwordError.value = 'La contraseña no cumple con los requisitos de seguridad (mínimo 12 caracteres, mayúsculas, minúsculas, números y símbolos).';
    return;
  }

  emit('save', { ...form }, isEdit.value);
};
</script>