# Proyecto: Sistema de Autenticación y Autorización (Master Gateway)

## URL del proyecto en Render: 

https://master-getway.onrender.com/login

![Render](./evidencias/deploy.png)


### Credenciales de prueba (para login en el frontend):
- Usuario: `administrador`
- Contraseña: `Vikingofarifor123.`

## Descripción

- Sistema compuesto por varios servicios backend (FastAPI) y un frontend (Vue 3 + Vite).
- Proporciona autenticación, autorización y gateway centralizado para otros servicios (ventas, entre otros).


## Servicios principales
- `auth-service` — API de autenticación, usuarios, roles, módulos y menús (FastAPI).
- `sale_service` — API de ventas (FastAPI).
- `master-getway` — Frontend en Vue 3 / Vite que consume las APIs.
- `db` y `redis` — servicios definidos en `docker-compose.yml` para desarrollo (Postgres + Redis).

## Tecnologías
- Backend: Python, FastAPI, SQLAlchemy (async), asyncpg/psycopg2, PyJWT.
- Frontend: Vue 3, Vite, PrimeVue.
- Infra: PostgreSQL, Redis, Docker Compose.

## Requisitos
- Python 3.13 (según configuración del proyecto) o una versión compatible.
- `pnpm` para el frontend.
- Docker & Docker Compose (para levantar Postgres/Redis en desarrollo).

# Quickstart (desarrollo)
1. Clona el repositorio:

	git clone <repo-url>
	cd ProyectoSoftwareSeguro-Parcial3

2. Crea un archivo `.env` en la raíz o en cada servicio con las variables necesarias (ejemplo abajo).

3. Correr el comando para crear las llaves con RSA y guardarlas en `shared-keys/shared-keys-private` y `shared-keys/shared-keys-public`:

```bash
bash shared-keys/keypair.sh
```

3. Levanta dependencias de infraestructura (Postgres y Redis):

	docker compose up -d

4. Backend - `auth-service`:

```bash
	cd auth-service
	python -m pip install -r requirements.txt
	uvicorn server:app --reload --port 8000
```
5. Backend - `sale_service`:

```bash
	cd ../sale_service
	python -m pip install -r requirements.txt
	uvicorn server:app --reload --port 8001
```
6. Frontend - `master-getway`:

```bash
	cd ../master-getway
	pnpm install   # o `npm install`
	pnpm dev       # o `npm run dev`
```

# Quickstart (desplegue con docker compose)

1. Clona el repositorio:

	git clone <repo-url>
	cd ProyectoSoftwareSeguro-Parcial3

2. Clona el archivo `.env.example` en la raíz y renómbralo a `.env`.

3. Correr el comando para crear las llaves con RSA y guardarlas en `shared-keys/shared-keys-private` y `shared-keys/shared-keys-public`:

```bash
bash shared-keys/keypair.sh
```

3. Levanta el contendor con todos los servicios (Postgres, Redis, backends y frontend):

```bash
  docker compose build
  docker compose up -d
```
## Notas sobre la base de datos
- El proyecto incluye `docker-compose.yml` que define `db` (Postgres) y `redis` para desarrollo.
- Al iniciar los backends, el servidor ejecuta la creación de tablas (Base.metadata.create_all) automáticamente.
- Si necesitas datos iniciales, ejecuta `db/insert.sql` contra la base.

## Tests
- Backend (auth-service / sale_service):

```bash
  cd auth-service
  python -m pip install -r requirements.txt
  pytest

  cd ../sale_service
  python -m pip install -r requirements.txt
  pytest
```

- Frontend (master-getway):

```bash
  cd master-getway
  pnpm test    # o `npm run test`
```

## Configuración y variables importantes
- `DATABASE_URL`: URL de conexión para SQLAlchemy async (ej: `postgresql+asyncpg://user:pass@host:5432/dbname`).
- `PORT`: puerto donde corre cada servicio (si se omite, los servidores usan 8000 por defecto).
- `REDIS_PORT` / `REDIS_URL`: configuración para rate limiting/cache.
- `JWT_SECRET` / `SECRET_KEY`: claves para firmar tokens y cifrado.

## Despliegue con Docker
- Para entornos de producción ajusta `docker-compose.yml`, las variables de entorno y añade volúmenes/backup según convenga.

- **Arquitectura de carpetas (detallada)**

```
ProyectoSoftwareSeguro-Parcial3/
├─ docker-compose.yml
├─ README.md
├─ sonar-project.properties
├─ auth-service/
│  ├─ server.py
│  ├─ requirements.txt
│  ├─ config/
│  │  ├─ database.py
│  │  ├─ rate_limit.py
│  │  └─ redis_cache.py
│  ├─ controllers/
│  │  ├─ auth_controller.py
│  │  ├─ internal_controller.py
│  │  ├─ menu_controller.py
│  │  ├─ module_controller.py
│  │  ├─ role_controller.py
│  │  └─ user_controller.py
│  ├─ dtos/
│  ├─ models/
│  ├─ repositories/
│  ├─ routes/
│  ├─ services/
│  └─ tests/
├─ sale_service/
│  ├─ server.py
│  ├─ requirements.txt
│  ├─ config/
│  ├─ controllers/
│  ├─ models/
│  ├─ repositories/
│  ├─ routes/
│  ├─ services/
│  └─ tests/
├─ master-getway/
│  ├─ package.json
│  ├─ src/
│  ├─ public/
│  └─ tests/
├─ db/
│  └─ insert.sql
├─ scripts/
└─ shared-keys/
```

**Consejos rápidos**
- Asegúrate de que las variables de entorno apunten a `db` cuando uses Docker Compose (host= db).
- Usa puertos distintos para servicios backend en desarrollo (8000, 8001, ...).
- Revisa `auth-service/config/database.py` para el formato esperado de `DATABASE_URL`.

## Integración con SonarCloud / SonarQube

El repositorio ya incluye `sonar-project.properties` con los parámetros básicos:

- `sonar.organization` y `sonar.projectKey`: identificadores en SonarCloud.
- `sonar.sources`: rutas que serán analizadas (por ejemplo `auth-service,sale_service,master-getway/src`).
- `sonar.exclusions`: patrones excluidos (node_modules, venv, archivos `.pem`, tests, etc.).
- `sonar.tests`: carpetas donde están los tests para asociar cobertura.
- `sonar.python.coverage.reportPaths` y `sonar.javascript.lcov.reportPaths`: rutas a los reportes de cobertura.

Ejecutar análisis con `sonar-scanner` (instala y configura `SONAR_TOKEN` en CI):

```bash
sonar-scanner \
	-Dsonar.projectKey=Sebas-Parra_ProyectoSoftwareSeguro-Parcial3 \
	-Dsonar.organization=sebas-parra \
	-Dsonar.host.url=https://sonarcloud.io \
	-Dsonar.login=$SONAR_TOKEN
```

También es común integrar SonarCloud mediante el action oficial en GitHub Actions (ver sección CI abajo).

## CI / Workflows

```yaml
# Notifica por Telegram los merges hacia las ramas de integracion (dev/test),
# tal como lo exige el Anexo del PDF. Usa los mismos secrets TELEGRAM_BOT_TOKEN
# y TELEGRAM_CHAT_ID que .github/workflows/ci-cd.yml.

name: Notificar Merge a dev/test

on:
  push:
    branches: [dev, test]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Telegram - merge exitoso
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d parse_mode="Markdown" \
            -d text="🔀 Merge exitoso hacia \`${{ github.ref_name }}\` - commit \`${{ github.sha }}\` por ${{ github.actor }}" || true

```


```yaml
# Pipeline CI/CD - Anexo "Requisitos de Infraestructura, CI/CD y DevSecOps"
# (PROY_PARCIAL_III_DesSeguro)
#
# Corre en cada push/merge a `main` y ejecuta, en orden, las 4 fases pedidas:
#   1. Build y Pruebas Unitarias
#   2. Analisis Estatico Tradicional (SonarCloud) - exige Quality Gate = OK
#   3. Analisis SAST Avanzado (modelo ML sobre archivos modificados)
#   4. Despliegue Automatico (Render), solo si 2 y 3 pasaron
#
# Secrets requeridos en Settings > Secrets and variables > Actions:
#   TELEGRAM_BOT_TOKEN     - token del bot creado con @BotFather
#   TELEGRAM_CHAT_ID       - id del grupo/canal de Telegram del equipo
#   SONAR_TOKEN            - token del proyecto en https://sonarcloud.io
#   HF_API_TOKEN           - token gratuito de https://huggingface.co/settings/tokens
#                            (opcional: si falta, la fase 3 se reporta como
#                            "sin analizar" y NO bloquea el pipeline)
#   RENDER_API_KEY         - API key personal de Render (Account Settings > API Keys)
#   RENDER_AUTH_SERVICE_ID     - service id (srv-xxxx) de auth-service en Render
#   RENDER_SALE_SERVICE_ID     - service id (srv-xxxx) de sale-service en Render
#   RENDER_FRONTEND_SERVICE_ID - service id (srv-xxxx) de master-getway en Render
#
# IMPORTANTE: en cada servicio de Render hay que desactivar "Auto-Deploy"
# (Settings > Auto-Deploy > No), para que el UNICO disparador de deploy sea
# este pipeline (y no el webhook automatico de Render en cada push), tal
# como exige el PDF.
#
# Mientras no existan las cuentas de SonarCloud/Render, este archivo queda
# igual de valido: las fases fallaran solo cuando ejecuten, con un mensaje
# claro sobre que secret falta.

name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  notify-start:
    name: Notificar inicio
    runs-on: ubuntu-latest
    steps:
      - name: Telegram - inicio del pipeline
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d parse_mode="Markdown" \
            -d text="🚀 *Pipeline iniciado* en \`main\` - commit \`${{ github.sha }}\` por ${{ github.actor }}" || true

  build-test:
    name: "Fase 1: Build y Pruebas Unitarias"
    needs: notify-start
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:alpine
        ports: ["6379:6379"]
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependencias - auth-service
        working-directory: auth-service
        run: pip install -r requirements.txt

      - name: Pruebas unitarias - auth-service
        working-directory: auth-service
        run: python -m pytest tests/ -v --cov=. --cov-report=xml:coverage.xml

      - name: Instalar dependencias - sale_service
        working-directory: sale_service
        run: pip install -r requirements.txt

      - name: Pruebas unitarias - sale_service
        working-directory: sale_service
        run: python -m pytest tests/ -v --cov=. --cov-report=xml:coverage.xml

      - name: Ajustar rutas de cobertura para que SonarCloud las encuentre
        run: |
          python scripts/fix_coverage_paths.py auth-service/coverage.xml auth-service
          python scripts/fix_coverage_paths.py sale_service/coverage.xml sale_service

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Habilitar pnpm
        run: corepack enable && corepack prepare pnpm@10.33.2 --activate

      - name: Instalar dependencias - frontend
        working-directory: master-getway
        run: pnpm install --frozen-lockfile

      - name: Pruebas unitarias - frontend
        working-directory: master-getway
        run: pnpm test

      - name: Build - frontend
        working-directory: master-getway
        run: pnpm build

      - name: Subir reportes de cobertura (para SonarCloud)
        uses: actions/upload-artifact@v4
        with:
          name: coverage-reports
          path: |
            auth-service/coverage.xml
            sale_service/coverage.xml
            master-getway/coverage/lcov.info
          retention-days: 1

      - name: Telegram - fallo en build/tests
        if: failure()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="❌ Build o pruebas unitarias fallaron en ${{ github.sha }}. Pipeline detenido." || true

  sonarcloud:
    name: "Fase 2: Analisis Estatico (SonarCloud)"
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Descargar reportes de cobertura
        uses: actions/download-artifact@v4
        with:
          name: coverage-reports

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

      - name: Esperar Quality Gate
        uses: sonarsource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

      - name: Telegram - Quality Gate OK
        if: success()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="✅ SonarCloud Quality Gate: PASSED (${{ github.sha }})" || true

      - name: Telegram - Quality Gate FAILED
        if: failure()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="❌ SonarCloud rechazo el codigo (Quality Gate FAILED). Pipeline detenido." || true

  ml-sast:
    name: "Fase 3: SAST Avanzado (Modelo ML)"
    needs: sonarcloud
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Analisis de mineria de datos sobre archivos modificados
        env:
          HF_API_TOKEN: ${{ secrets.HF_API_TOKEN }}
          BASE_SHA: ${{ github.event.before }}
          HEAD_SHA: ${{ github.sha }}
        run: python scripts/ml_sast_scan.py

      - name: Telegram - alerta critica del modelo ML
        if: failure()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="🚨 ALERTA: el modelo de mineria de datos detecto un patron sospechoso de vulnerabilidad en ${{ github.sha }}. Pipeline detenido." || true

  deploy:
    name: "Fase 4: Despliegue Automatico (Render)"
    needs: ml-sast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Telegram - iniciando despliegue
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="🛡️ Seguridad validada. Desplegando ${{ github.sha }} a Render..." || true

      # scripts/render_deploy.py dispara el deploy via la API de Render y
      # espera (polling) a que termine, para poder reportar exito/fallo real
      # (no solo "se disparo"). Requiere que Auto-Deploy este DESACTIVADO en
      # cada servicio de Render, para que el unico disparador sea este job.
      - name: Deploy auth-service
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: python scripts/render_deploy.py "${{ secrets.RENDER_AUTH_SERVICE_ID }}"

      - name: Deploy sale-service
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: python scripts/render_deploy.py "${{ secrets.RENDER_SALE_SERVICE_ID }}"

      - name: Deploy frontend
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: python scripts/render_deploy.py "${{ secrets.RENDER_FRONTEND_SERVICE_ID }}"

      - name: Telegram - despliegue exitoso
        if: success()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="🎉 Despliegue en produccion exitoso (${{ github.sha }})." || true

      - name: Telegram - despliegue fallido
        if: failure()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id="${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d text="❌ Fallo el despliegue a Render (${{ github.sha }})." || true


```

Notas:
- Define el secreto `SONAR_TOKEN` en los Secrets del repositorio con un token de SonarCloud.
- Ajusta versiones de Python/Node según tu entorno.
- Puedes combinar pasos, cachear dependencias y subir artefactos de cobertura para Sonar.

