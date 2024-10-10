# LinkScribe - Organizador de Enlaces Inteligente

LinkScribe es una aplicación que permite a los usuarios organizar y gestionar enlaces web automáticamente utilizando procesamiento de lenguaje natural (NLP). Esta documentación cubre cómo ejecutar la aplicación en un entorno local utilizando Docker y Docker Compose.

## Requisitos

- [Docker](https://www.docker.com/get-started) instalado.
- [Docker Compose](https://docs.docker.com/compose/) instalado.
- Una cuenta de servicio en Google Cloud con acceso a Google Cloud Storage.
- Archivo `service-account.json` con las credenciales de la cuenta de servicio.

## Configuración

### 1. Configurar Google Cloud Storage

1. Ve a la [Consola de Google Cloud](https://console.cloud.google.com/).
2. Crea un bucket de Google Cloud Storage y toma nota del nombre.
3. Descarga las credenciales de la cuenta de servicio y guárdalas en `./backend/credentials/service-account.json`.

### 2. Configuración del archivo `docker-compose.yml`

Edita el archivo `docker-compose.yml` para incluir:
- Tu nombre de bucket en `GCS_BUCKET_NAME`.
- El archivo de credenciales en el volumen `./backend/credentials:/app/credentials`.

### 3. Base de Datos

El entorno utiliza PostgreSQL como base de datos. Asegúrate de actualizar el archivo `docker-compose.yml` con tus credenciales de base de datos:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

### Ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/linkscribe.git
   cd linkscribe
