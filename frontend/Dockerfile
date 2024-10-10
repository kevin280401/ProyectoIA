# frontend/Dockerfile

# Etapa de construcción
FROM node:16-alpine AS build

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de package.json y package-lock.json
COPY package.json package-lock.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos de la aplicación
COPY . .

# Construye la aplicación para producción
RUN npm run build

# Etapa de producción
FROM nginx:alpine

# Copia los archivos construidos desde la etapa de construcción
COPY --from=build /app/build /usr/share/nginx/html

# Copia la configuración personalizada de Nginx (si tienes una)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80
EXPOSE 80

# Comando por defecto para ejecutar Nginx
CMD ["nginx", "-g", "daemon off;"]
