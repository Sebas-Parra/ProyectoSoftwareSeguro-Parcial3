<template>
    
    <Card class="container-login">
        <template #header>
            <div class="container-login-card">
                <img alt="user header" src="@/assets/LogoBi.png" class="img-logo" />
            </div>
        </template>
        <template #content>
            <div class="container-login-card">
                <IftaLabel class="login-div">
                    <IconField>
                        <InputIcon class="pi pi-user" />
                        <InputText id="emailuser" v-model="username" class="components-login" @keypress.enter="login()" :disabled="isLoading"/>
                    </IconField>
                    <label for="emailuser">Usuario</label>
                </IftaLabel>
            </div>
            <div class="container-login-card">
                <IftaLabel class="login-div">
                    <IconField>
                        <InputIcon class="pi pi-lock" />
                        <Password id="password" v-model="password" toggleMask :feedback="false" class="components-login" @keypress.enter="login()" :disabled="isLoading"/>
                    </IconField>
                    <label for="password">Contraseña</label>
                </IftaLabel>
            </div>
            <div class="container-login-card">
                <Button label="INICIAR SESIÓN" icon="pi pi-sign-in" class="boton" severity="danger" @click="login()" :loading="isLoading" :disabled="isLoading"/>
            </div>
        </template>
    </Card>
    
    <!-- Loading Overlay with Spinner -->
    <div v-if="isLoading" class="loading-overlay">
        <ProgressSpinner 
            style="width: 40%; height: 40%;" 
            strokeWidth="8" 
            fill="transparent"
            animationDuration=".5s" 
            aria-label="Custom ProgressSpinner" 
        />
    </div>
    <Toast position="bottom-right" style="width: auto; margin-left: 5vw;"/>
</template>

<script setup>

import Password from 'primevue/password';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import IftaLabel from 'primevue/iftalabel';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import ProgressSpinner from 'primevue/progressspinner';
import Card from 'primevue/card';
import Toast from 'primevue/toast';
import { useAuth } from '@/helpers/useAuth.js';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToastGlobal } from '@/helpers/utils.js';


const router = useRouter();
const { login: authLogin } = useAuth();
const { msjShow } = useToastGlobal();

const username = ref('');
const password = ref('');
const isLoading = ref(false);

const login = async () => {

    // 1. Validación básica de campos vacíos
    if (!username.value.trim() || !password.value.trim()) {
        msjShow('error', 'Campos requeridos', 'Por favor complete todos los campos', 3000);
        return; // Detenemos la ejecución
    }

    isLoading.value = true;

    try {
        // 2. Llamada al servicio de autenticación
        await authLogin(username.value, password.value);

        msjShow('success', 'Éxito', 'Inicio de sesión exitoso', 2000);

        // 3. Si todo sale bien, redirigimos después de 1 segundo
        setTimeout(1000);
        router.push('/home');
        
    } catch (error) {
        // 4. Capturamos errores 
        msjShow('error', 'Error al iniciar sesión', error || 'Credenciales incorrectas', 4000);
    } finally {
        isLoading.value = false;
    }
};


</script>

<style scoped>

::v-deep(.p-password-input) {
    width: 100% !important;
}

.container-login {
    width: 100%;
    max-width: 25rem;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

</style>