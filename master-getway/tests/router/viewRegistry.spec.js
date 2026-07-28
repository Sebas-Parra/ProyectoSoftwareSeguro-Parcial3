import { describe, it, expect } from 'vitest';
import viewRegistry from '@/router/viewRegistry.js';

describe('viewRegistry', () => {
    it('expone un loader de componente (funcion) para cada vista conocida', () => {
        const expectedKeys = ['admin/menus', 'admin/roles', 'admin/users', 'admin/modules', 'sales'];

        expectedKeys.forEach((key) => {
            expect(typeof viewRegistry[key]).toBe('function');
        });
    });

    it('no tiene una entrada para rutas que no existen', () => {
        expect(viewRegistry['ruta-inventada']).toBeUndefined();
    });

    it('cada loader realmente resuelve un componente Vue valido', async () => {
        for (const key of Object.keys(viewRegistry)) {
            const mod = await viewRegistry[key]();
            expect(mod.default).toBeDefined();
        }
    });
});
