# Imagen base para desarrollo y compilación del frontend con Vite.
FROM node:24-alpine AS base
WORKDIR /app

# Se copian primero los manifiestos para aprovechar la caché de Docker.
COPY package*.json ./
RUN npm ci

COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Etapa de compilación para producción.
FROM base AS build
RUN npm run build

# Etapa final: sirve los archivos estáticos con Nginx.
FROM nginx:1.27-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
