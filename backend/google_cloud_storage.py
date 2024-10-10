from google.cloud import storage
import os

# Inicializa el cliente de Google Cloud Storage
def init_storage_client():
    return storage.Client()

# Subir un archivo a Google Cloud Storage
def upload_file_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """Sube un archivo a un bucket de Google Cloud Storage."""
    try:
        client = init_storage_client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_path)
        print(f"File {source_file_path} uploaded to {destination_blob_name}.")
        return True
    except Exception as e:
        print(f"Failed to upload file: {e}")
        return False

# Descargar un archivo desde Google Cloud Storage
def download_file_from_gcs(bucket_name, source_blob_name, destination_file_path):
    """Descarga un archivo desde un bucket de Google Cloud Storage."""
    try:
        client = init_storage_client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_path)
        print(f"Blob {source_blob_name} downloaded to {destination_file_path}.")
        return True
    except Exception as e:
        print(f"Failed to download file: {e}")
        return False

# Listar archivos en un bucket
def list_files_in_bucket(bucket_name):
    """Lista todos los archivos en un bucket de Google Cloud Storage."""
    try:
        client = init_storage_client()
        blobs = client.list_blobs(bucket_name)
        
        file_list = [blob.name for blob in blobs]
        print(f"Files in bucket {bucket_name}: {file_list}")
        return file_list
    except Exception as e:
        print(f"Failed to list files: {e}")
        return []

# Eliminar un archivo de Google Cloud Storage
def delete_file_from_gcs(bucket_name, blob_name):
    """Elimina un archivo de un bucket de Google Cloud Storage."""
    try:
        client = init_storage_client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()
        print(f"Blob {blob_name} deleted.")
        return True
    except Exception as e:
        print(f"Failed to delete file: {e}")
        return False
