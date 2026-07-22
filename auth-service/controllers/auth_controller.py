from fastapi import HTTPException, status, Security
from sqlalchemy.orm import Session
from services import auth_service, jwt_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

async def select_role_controller(db: Session, role_data, credentials: HTTPAuthorizationCredentials):

    token = credentials.credentials

    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)

    try: 
        
        response = await auth_service.select_role_service(db, int(payload['sub']), role_data.role_id)
        
        if not response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario o rol no válido"
            )
        
        access_token, refresh_token = response
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        print(f"Error en select_role_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor"
        )

async def refresh_token_controller(credentials: HTTPAuthorizationCredentials):

    token = credentials.credentials

    response, error = await jwt_service.validar_refresh_token(token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try: 
            
        access_token, refresh_token = response

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        print(f"Error en refresh_token_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor"
        )

async def logout_controller(credentials: HTTPAuthorizationCredentials):
    
    token = credentials.credentials

    print(f"Token recibido en logout_controller: {token}")

    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)
    
    try: 
        jti = payload.get("jti")
        
        if jti:
            await jwt_service.delete_tokens(jti)
            return {"message": "Sesión cerrada exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Token inválido o sin jti")
    except Exception as e:
        print(f"Error en logout_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor"
        )

async def login_controller(db: Session, login_data):

    response = await auth_service.login_user_service(db, login_data.username, login_data.password)
    
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    try: 
        
        temp_token, roles = response
        return {
            "temp_token": temp_token,
            "token_type": "bearer",
            "roles": roles
        }
    
    except Exception as e:
        print(f"Error en login_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor"
        )