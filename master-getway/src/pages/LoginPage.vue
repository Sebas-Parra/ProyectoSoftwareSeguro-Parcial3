<template>
  <div class="login-page">
    <div class="cloud-path"></div>

    <div class="login-wrapper">
      <FormLogin />
    </div>
  </div>
</template>

<script setup>
import FormLogin from '@/components/form/FormLogin.vue';
</script>

<style scoped>
.login-page {
  position: relative;
  overflow: hidden;
  display: flex;
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  background: #091350; /* Tu azul oscuro */
}

/* La forma de nube nítida y orgánica usando clip-path */
.cloud-path {
  position: absolute;
  bottom: -20px; /* Ajuste para esconder el borde inferior */
  left: 0;
  width: 100%;
  height: 250px; /* Altura de la masa blanca */
  background: white; /* Color sólido y nítido */
  
  /* --- ESTO ES LA MAGIA: Define el contorno orgánico --- */
  /* Recrea la forma de tu imagen de referencia */
  clip-path: ellipse(65% 120% at 50% 120%); 
}

.login-wrapper {
  z-index: 10; /* Asegura que el formulario esté por encima */
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>