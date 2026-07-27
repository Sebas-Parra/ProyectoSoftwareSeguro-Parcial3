import { describe, it, expect, afterEach, vi } from 'vitest';
import router from '@/router/router.js';

vi.mock('@/services/menuService.js', () => ({
    menuService: { getMenusTree: vi.fn() },
}));

import { menuService } from '@/services/menuService.js';
import { useMenu, registerRoutesFromMenu, clearDynamicRoutes } from '@/helpers/useMenu.js';

const sampleTree = [
    {
        id: 1, nombre: 'Administración', url: null, children: [
            { id: 2, nombre: 'Usuarios', url: '/home/admin/users', children: [] },
            { id: 3, nombre: 'Ventas', url: '/home/sales', children: [] },
        ],
    },
];

describe('registerRoutesFromMenu', () => {
    afterEach(() => {
        clearDynamicRoutes();
    });

    it('registra rutas dinamicas solo para los items hoja con vista conocida', () => {
        registerRoutesFromMenu(sampleTree);

        expect(router.hasRoute('dynamic-admin/users')).toBe(true);
        expect(router.hasRoute('dynamic-sales')).toBe(true);

        const resolved = router.resolve('/home/admin/users');
        expect(resolved.name).toBe('dynamic-admin/users');
    });

    it('no registra ruta para los nodos padre (sin url)', () => {
        registerRoutesFromMenu(sampleTree);

        expect(router.hasRoute('dynamic-null')).toBe(false);
        expect(router.getRoutes().some((r) => r.name === 'dynamic-undefined')).toBe(false);
    });

    it('ignora items cuyo url no tiene vista registrada en viewRegistry', () => {
        const treeWithUnknownView = [
            { id: 9, nombre: 'Reportes', url: '/home/reportes-financieros', children: [] },
        ];

        registerRoutesFromMenu(treeWithUnknownView);

        expect(router.hasRoute('dynamic-reportes-financieros')).toBe(false);
    });

    it('ignora items con url externa (http)', () => {
        const treeWithExternalLink = [
            { id: 10, nombre: 'Externo', url: 'https://ejemplo.com', children: [] },
        ];

        registerRoutesFromMenu(treeWithExternalLink);

        expect(router.getRoutes().some((r) => r.name === 'dynamic-https://ejemplo.com')).toBe(false);
    });

    it('clearDynamicRoutes elimina las rutas previamente registradas', () => {
        registerRoutesFromMenu(sampleTree);
        expect(router.hasRoute('dynamic-admin/users')).toBe(true);

        clearDynamicRoutes();

        expect(router.hasRoute('dynamic-admin/users')).toBe(false);
        expect(router.hasRoute('dynamic-sales')).toBe(false);
    });

    it('registrar un menu nuevo limpia las rutas del rol/menu anterior', () => {
        registerRoutesFromMenu(sampleTree);
        expect(router.hasRoute('dynamic-sales')).toBe(true);

        const otherTree = [{ id: 4, nombre: 'Roles', url: '/home/admin/roles', children: [] }];
        registerRoutesFromMenu(otherTree);

        expect(router.hasRoute('dynamic-sales')).toBe(false);
        expect(router.hasRoute('dynamic-admin/users')).toBe(false);
        expect(router.hasRoute('dynamic-admin/roles')).toBe(true);
    });

    it('no falla si el arbol de menu no es un arreglo', () => {
        expect(() => registerRoutesFromMenu(null)).not.toThrow();
        expect(() => registerRoutesFromMenu(undefined)).not.toThrow();
    });
});

describe('fetchMenu', () => {
    afterEach(() => {
        clearDynamicRoutes();
        localStorage.clear();
        vi.clearAllMocks();
    });

    it('guarda el menu devuelto por el backend, lo persiste y registra las rutas', async () => {
        menuService.getMenusTree.mockResolvedValue({ data: sampleTree });

        const { fetchMenu, menu } = useMenu();
        await fetchMenu();

        expect(menu.value).toEqual(sampleTree);
        expect(JSON.parse(localStorage.getItem('menu'))).toEqual(sampleTree);
        expect(router.hasRoute('dynamic-admin/users')).toBe(true);
    });

    it('si la API falla, no lanza y no rompe la app', async () => {
        menuService.getMenusTree.mockRejectedValue(new Error('network error'));

        const { fetchMenu } = useMenu();

        await expect(fetchMenu()).resolves.toBeUndefined();
    });
});
