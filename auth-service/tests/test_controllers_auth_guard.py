"""
Prueba, para cada controlador de auth-service, que un token invalido (o
directamente basura) sea rechazado con 401 ANTES de tocar la base de datos.
Esto ejercita el guard de Zero Trust ("Validacion obligatoria en cada
endpoint") a nivel de cada controlador.
"""
import types

import pytest
from fastapi import HTTPException

from tests.db_helpers import run
from controllers import auth_controller, user_controller, role_controller, module_controller, menu_controller, internal_controller


def _bad_credentials():
    return types.SimpleNamespace(credentials="esto-no-es-un-jwt-valido")


CASES = [
    ("auth.select_role", lambda: auth_controller.select_role_controller(None, types.SimpleNamespace(role_id=1), _bad_credentials())),
    ("auth.refresh_token", lambda: auth_controller.refresh_token_controller(_bad_credentials())),
    ("auth.logout", lambda: auth_controller.logout_controller(_bad_credentials())),

    ("user.get_all", lambda: user_controller.get_all_users_controller(None, 1, 10, _bad_credentials())),
    ("user.get_by_id", lambda: user_controller.get_user_by_id_controller(None, 1, _bad_credentials())),
    ("user.register", lambda: user_controller.register_user_controller(None, "juan", "Pass1234!", _bad_credentials())),
    ("user.update", lambda: user_controller.update_user_controller(None, 1, "juan", "Pass1234!", _bad_credentials())),
    ("user.delete", lambda: user_controller.delete_user_controller(None, 1, _bad_credentials())),

    ("role.get_all", lambda: role_controller.get_all_roles_controller(None, _bad_credentials())),
    ("role.update", lambda: role_controller.update_role_controller(None, 1, None, _bad_credentials())),
    ("role.delete", lambda: role_controller.delete_role_controller(None, 1, _bad_credentials())),
    ("role.assign_to_user", lambda: role_controller.asign_role_to_user_controller(None, 1, 1, _bad_credentials())),
    ("role.unassign_from_user", lambda: role_controller.desasign_role_from_user_controller(None, 1, 1, _bad_credentials())),
    ("role.insert", lambda: role_controller.insert_role_controller(None, None, _bad_credentials())),

    ("module.get_all", lambda: module_controller.get_all_modules_controller(None, _bad_credentials())),
    ("module.insert", lambda: module_controller.insert_module_controller(None, None, _bad_credentials())),
    ("module.update", lambda: module_controller.update_module_controller(None, 1, None, _bad_credentials())),
    ("module.delete", lambda: module_controller.delete_module_controller(None, 1, _bad_credentials())),
    ("module.assign_to_role", lambda: module_controller.assign_module_to_role_controller(None, 1, 1, _bad_credentials())),

    ("menu.get_tree", lambda: menu_controller.get_active_menus_flat_controller(None, _bad_credentials())),
    ("menu.create", lambda: menu_controller.create_menu_controller(None, None, _bad_credentials())),
    ("menu.update", lambda: menu_controller.update_menu_controller(None, 1, None, _bad_credentials())),
    ("menu.delete", lambda: menu_controller.delete_menu_controller(None, 1, _bad_credentials())),
    ("menu.assign_to_role", lambda: menu_controller.insert_role_menu_controller(None, 1, 1, _bad_credentials())),
    ("menu.get_all", lambda: menu_controller.get_all_menus_controller(None, _bad_credentials())),

    ("internal.validate_token", lambda: internal_controller.validate_token_controller(_bad_credentials())),
]


@pytest.mark.parametrize("name,call", CASES, ids=[c[0] for c in CASES])
def test_controller_rejects_invalid_token(name, call):
    with pytest.raises(HTTPException) as exc_info:
        run(call())

    assert exc_info.value.status_code == 401
