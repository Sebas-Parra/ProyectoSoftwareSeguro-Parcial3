import { describe, it, expect } from 'vitest';
import router from '@/router/router.js';

describe('router', () => {
    it('la ruta /home no tiene children hardcodeados (se agregan en runtime segun el menu)', () => {
        const homeRoute = router.getRoutes().find((r) => r.name === 'home');

        expect(homeRoute).toBeTruthy();
        expect(homeRoute.children.length).toBe(0);
    });

    it('la ruta /login existe y es publica (requiresGuest)', () => {
        const loginRoute = router.getRoutes().find((r) => r.name === 'login');

        expect(loginRoute).toBeTruthy();
        expect(loginRoute.meta.requiresGuest).toBe(true);
    });

    it('las rutas desconocidas redirigen a /login', () => {
        const resolved = router.resolve('/una-ruta-que-no-existe');

        expect(resolved.matched[0].redirect).toBe('/login');
    });
});
