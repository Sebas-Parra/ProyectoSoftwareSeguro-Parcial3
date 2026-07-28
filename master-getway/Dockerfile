# --- Etapa 1: Construcción (Build) ---
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json pnpm-lock.yaml ./

RUN npm install -g pnpm && pnpm install --frozen-lockfile

COPY . .

# Usamos valores comodín durante el build que luego serán reemplazados
ENV VITE_API_AUTH_URL=__VITE_API_AUTH_URL__
ENV VITE_API_CRUD_URL=__VITE_API_CRUD_URL__
ENV VITE_API_TIMEOUT=__VITE_API_TIMEOUT__

RUN pnpm build

# --- Etapa 2: Servidor Web de Producción ---
FROM nginx:alpine

# Copiar archivos compilados
COPY --from=build /app/dist /usr/share/nginx/html

# Configuración Nginx para soporte de Vue Router (modo history)
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Script que reemplaza los comodines por las variables reales del .env al iniciar el contenedor
CMD ["/bin/sh", "-c", "for file in /usr/share/nginx/html/assets/*.js; do \
  sed -i \"s|__VITE_API_AUTH_URL__|${VITE_API_AUTH_URL}|g\" $file; \
  sed -i \"s|__VITE_API_CRUD_URL__|${VITE_API_CRUD_URL}|g\" $file; \
  sed -i \"s|__VITE_API_TIMEOUT__|${VITE_API_TIMEOUT}|g\" $file; \
  done && nginx -g 'daemon off;'"]