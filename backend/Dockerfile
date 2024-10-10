# backend/Dockerfile

# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece variables de entorno para evitar la escritura de bytecode y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Actualiza el sistema e instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos al contenedor
COPY requirements.txt .

# Actualiza pip a la última versión
RUN pip install --upgrade pip

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Descarga los recursos de NLTK
RUN python -m nltk.downloader stopwords punkt

# Copia el resto de los archivos de la aplicación al contenedor
COPY . .

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación usando gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
