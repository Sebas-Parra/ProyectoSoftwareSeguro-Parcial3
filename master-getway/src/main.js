import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import router from '@/router/router.js';
import 'primeicons/primeicons.css'
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import '@/css/general.css'

createApp(App)
.use(router)
.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.my-app-dark',
        }
    }
})
.use(ConfirmationService)
.use(ToastService)
.mount('#app')