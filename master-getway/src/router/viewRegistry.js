/**
 * Catalogo de vistas disponibles en el frontend, indexadas por la ruta
 * relativa a "/home/" que el backend (Master) puede devolver en el campo
 * `url` de un item de menu.
 *
 * Esto NO es una lista de rutas hardcodeadas: el router no registra nada de
 * aqui por adelantado. Es solo el mapa de "que componente existe" para que,
 * cuando el arbol de menu llegue desde el backend tras seleccionar el rol,
 * se puedan registrar dinamicamente (via router.addRoute) unicamente las
 * rutas que ese rol realmente tiene asignadas.
 *
 * Si el backend agrega un menu nuevo cuyo `url` no esta aqui, la app no se
 * rompe: simplemente ese item de menu no navega a ninguna vista todavia
 * (hace falta programar la pantalla correspondiente y agregarla aqui).
 */
const viewRegistry = {
    'admin/menus': () => import('@/pages/MenuPage.vue'),
    'admin/roles': () => import('@/pages/RolePage.vue'),
    'admin/users': () => import('@/pages/UserPage.vue'),
    'admin/modules': () => import('@/pages/ModulePage.vue'),
    'sales': () => import('@/pages/SalePage.vue'),
};

export default viewRegistry;
