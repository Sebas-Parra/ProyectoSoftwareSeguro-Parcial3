-- REGISTRO DEL ROL ADMINISTRADOR POR DEFECTO

INSERT INTO roles (name, description, status, icon, created_by, updated_by)
VALUES ('administrador', 'Es el rol de administrador', true ,'pi-crown', null, null);

INSERT INTO users (username, password, status)
VALUES ('administrador', '$2b$12$08j2I.mdR1JHL5q18iTBZuIjRtsFI03lq30Ugg1lx0KHMn33ZwNXe', true);

INSERT INTO user_roles (user_id, role_id) VALUES (1, 1);

INSERT INTO modules (name, description, icon, status, created_by, updated_by)
VALUES ('Administración', 'Módulo principal de control y seguridad del sistema', 'pi-shield', true, 1, 1);

-- Modulo separado para el microservicio de Ventas: sale_service exige que
-- el rol tenga ESTE modulo asignado para autorizar (403 si no lo tiene).
INSERT INTO modules (name, description, icon, status, created_by, updated_by)
VALUES ('Ventas', 'Módulo de gestión de ventas', 'pi-shopping-cart', true, 1, 1);

INSERT INTO menus (nombre, url, modulo_id, parent_id, status, created_by, updated_by)
VALUES ('Administración', null, 1, NULL, true, 1, 1);


INSERT INTO menus (nombre, url, modulo_id, parent_id, status, created_by, updated_by) VALUES
('Usuarios', '/home/admin/users', 1, 1, true, 1, 1),
('Roles', '/home/admin/roles', 1, 1, true, 1, 1),
('Módulos', '/home/admin/modules', 1, 1, true, 1, 1),
('Menús', '/home/admin/menus', 1, 1, true, 1, 1),
('Ventas', '/home/sales', 2, 1, true, 1, 1);


INSERT INTO role_modules (role_id, module_id, status, created_by, updated_by)
VALUES (1, 1, true, 1, 1),
       (1, 2, true, 1, 1);

INSERT INTO role_menus (role_id, menu_id) VALUES 
(1, 1), -- Menú raíz: Administración
(1, 2), -- Menú hijo: Usuarios
(1, 3), -- Menú hijo: Roles
(1, 4), -- Menú hijo: Módulos
(1, 5), -- Menú hijo: Menús
(1, 6); -- Menú hijo: Ventas