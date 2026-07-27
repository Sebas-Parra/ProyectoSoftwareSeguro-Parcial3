from models.user_model import User
from models.role_model import Role
from models.module_model import Module
from models.menu_model import Menu
from models.user_roles_model import UserRole
from models.role_modules_model import RoleModule
from models.role_menu_model import RoleMenu


def test_user_model_instantiation():
    user = User(username="juan", password="hash")
    assert user.username == "juan"


def test_role_model_instantiation():
    role = Role(name="vendedor", description="rol de ventas", icon="pi-user")
    assert role.name == "vendedor"


def test_module_model_instantiation():
    module = Module(name="Ventas", icon="pi-cart", description="modulo de ventas")
    assert module.name == "Ventas"


def test_menu_model_instantiation():
    menu = Menu(nombre="Ventas", url="/home/sales", modulo_id=1, parent_id=None)
    assert menu.parent_id is None


def test_user_role_pivot_instantiation():
    pivot = UserRole(user_id=1, role_id=2)
    assert pivot.user_id == 1
    assert pivot.role_id == 2


def test_role_module_pivot_instantiation():
    pivot = RoleModule(role_id=1, module_id=2)
    assert pivot.role_id == 1
    assert pivot.module_id == 2


def test_role_menu_pivot_instantiation():
    pivot = RoleMenu(role_id=1, menu_id=6)
    assert pivot.role_id == 1
    assert pivot.menu_id == 6


def test_role_menu_pivot_has_audit_fields():
    """role_menus no debe ser una 'tabla tonta': igual que user_roles y
    role_modules, debe tener created_by/updated_by (y status, igual que
    role_modules) para saber cuando y quien otorgo el permiso."""
    pivot = RoleMenu(role_id=1, menu_id=6, created_by=1, updated_by=1)
    assert pivot.created_by == 1
    assert pivot.updated_by == 1
    assert hasattr(pivot, "status")
