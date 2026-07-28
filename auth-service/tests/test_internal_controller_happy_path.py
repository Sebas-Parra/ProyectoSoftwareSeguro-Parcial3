from tests.db_helpers import run, DbCase
from tests.auth_test_helpers import make_admin_context, bearer
from controllers import internal_controller


def test_validate_token_returns_user_and_role_without_sensitive_data():
    async def scenario():
        async with DbCase() as db:
            user, role, access_token, _ = await make_admin_context(db)

            response = await internal_controller.validate_token_controller(bearer(access_token))

            assert response == {"valid": True, "user_id": user.id, "role_id": role.id}
            # No debe filtrar datos sensibles (password, username, etc.)
            assert "password" not in response
            assert "username" not in response

    run(scenario())


def test_validate_token_rejects_expired_token():
    import time
    import jwt as pyjwt
    from services import jwt_service
    from fastapi import HTTPException

    async def scenario():
        now = int(time.time())
        expired_payload = {
            "sub": "1", "username": "administrador", "type": "access",
            "role_id": 1, "exp": now - 60, "iat": now - 120,
        }
        expired_token = pyjwt.encode(expired_payload, jwt_service.PRIVATE_KEY, algorithm=jwt_service.ALGORITHM)

        try:
            await internal_controller.validate_token_controller(bearer(expired_token))
            assert False, "deberia haber lanzado HTTPException"
        except HTTPException as exc:
            assert exc.status_code == 401

    run(scenario())
