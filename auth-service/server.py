import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import Base, engine
import models
import routes
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from config.rate_limit import limiter
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# 1. Definir la función para crear las tablas usando run_sync
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 2. Configurar el evento de arranque de FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta antes de que el servidor empiece a recibir peticiones
    await init_models()
    yield
    # (Lo que pongas después del yield se ejecutaría al apagar el servidor)

# 3. Pasar el lifespan al crear la app
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173", # Puerto por defecto de Vite / Vue
    "http://localhost:3000", # Por si usas otro entorno o puerto local
    "https://master-getway.onrender.com/login"
    # Agrega aquí los dominios de producción si los tienes, ej: "https://tudominio.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Orígenes permitidos (puedes usar ["*"] para permitir todos en desarrollo)
    allow_credentials=True,     # Permitir envío de cookies / credenciales (necesario si manejas cookies HttpOnly)
    allow_methods=["*"],        # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],        # Permitir todos los headers (Authorization, Content-Type, etc.)
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Incluir rutas
app.include_router(routes.auth_routes.router)
app.include_router(routes.user_routes.router)
app.include_router(routes.role_routes.router)
app.include_router(routes.module_routes.router)
app.include_router(routes.menu_route.router)
app.include_router(routes.internal_routes.router)

# 4. Bloque para ejecutar Uvicorn leyendo el puerto de las variables de entorno
if __name__ == "__main__":
    import uvicorn
    # Lee la variable PORT del archivo .env; si no existe, por defecto usa el puerto 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="127.0.0.1", port=port, reload=True)